from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from .serializer import *
from opt_module.serializer import *
from cliente.models import  Cliente
import cliente
from .numContaGenerator import generate_unique_numconta
from opt_module.messageGenerator import mensagem_de_abertura_de_conta
from opt_module.myOtp import send_messages
from django.contrib.auth.models import User
from agente.models import Agente
from django.db import transaction
from operacao.models import Operacao
from operacao.serializer import OperacaoSerializer
from deposito.models import Deposito
from levantamento.models import Levantamento
from deposito.serializer import DepositoSerializer
from levantamento.serializer import LevantamentoSerializer
from transferencia.models import Transferencia
from transferencia.serializer import TransferenciaSerializer
from django.http import HttpResponse,JsonResponse,FileResponse
from utilizador.serializer import UserSerializer
# Create your views here.


#retorna todas operacoes envolvendo a uma determinada conta
def getExtrato(conta):
    depositos = Deposito.objects.all()
    levantamentos =  Levantamento.objects.all()
    transferencias = Transferencia.objects.all()
    extratoList = []
    operacaoes = Operacao.objects.all()
    for op in operacaoes:
        for d in depositos:
            #verifica se o deposito foi feito com aquela conta enviada por parametro
            if d.id_operacao.id_conta.id==conta.id and op.id==d.id_operacao.id:
                    depSer = DepositoSerializer(d,many=False)
                    depDict = depSer.data
                    depDict["valor"] = op.valor
                    depDict["Data"] = op.data_operacao
                    depDict["operacao"] = "DEPOSITO"
                    extratoList.append(depDict)
                    break
        for l in levantamentos:
            #verifica se o levantamento foi feito com aquela conta
            if l.id_operacao.id_conta.id==conta.id and op.id==l.id_operacao.id:
                    levSer = LevantamentoSerializer(l,many=False)
                    levDict = levSer.data
                    levDict["valor"] = op.valor
                    levDict["Data"] = op.data_operacao
                    levDict["operacao"] = "LEVANTAMENTO"
                    extratoList.append(levDict)
                    break
        for t in transferencias:
            #verifica se o transferencia foi feito com aquela conta
            if t.id_operacao.id_conta.id==conta.id and op.id==t.id_operacao.id:
                    transSer = TransferenciaSerializer(t,many=False)
                    transDict = transSer.data
                    transDict["valor"] = op.valor
                    transDict["Data"] = op.data_operacao
                    transDict["operacao"] = "TRANSFERÊNCIA"
                    extratoList.append(transDict)
                    break
#verifica se aquela operacao foi de um dinheiro que a conta recebeu
        #verificar se aquela operacao é uma transferencia
        trans = Transferencia.objects.filter(id_operacao=op.id).first()
        if trans:
            #verificar se a transferencia foi feita por uma conta diferente da conta passada por parametro
            if trans.id_operacao.id_conta.numero != conta.numero:
                #verificar se a numero de conta na operacao dessa transferencia, é o mesmo que o numero da conta passada por parametro
                if trans.numero_conta == conta.numero:
                    t = trans
                    transSer = TransferenciaSerializer(trans,many=False)
                    transDict = transSer.data
                    transDict["valor"] = t.id_operacao.valor
                    transDict["Data"] = t.id_operacao.data_operacao
                    transDict["operacao"] = "RECEBEU"
                    transDict["origem"] = t.id_operacao.id_conta.id_client.id_user.first_name+" "+t.id_operacao.id_conta.id_client.id_user.last_name
                    extratoList.append(transDict)       
    #inverte a lista para deixar o extrato na ordem decrescente
    extratoList.reverse()    
    return extratoList
    
#retorna o ID do titular de uma conta
#ALL
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getContaTitularID(request,numero_conta):
    conta = Conta.objects.filter(numero=numero_conta).first()
    if conta:
        client =  Cliente.objects.filter(id=conta.id_client.id).first()
        if client:
            user = User.objects.get(id=client.id_user.id)
            userSerializer =  UserSerializer(user,many=False)
            limitedData = userSerializer.data
            limitedData.pop("password")
            return Response(limitedData)
    return Response({"error":"Not found"}, status=status.HTTP_404_NOT_FOUND)


#retorna o extrado bancario de uma conta
#ADMIN, CLIENT(id_client=id_client)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getExtratoConta(request,id_conta):
    conta = None
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #
    cli = Cliente.objects.filter(id_user=user.id).first()
    if cli:
        conta = Conta.objects.filter(id_client=cli.id, id=id_conta).first()
    elif user.is_superuser:
        conta = Conta.objects.filter(id=id_conta).first()
    if conta:
            #pega todas as operacoes relacionadas com essa conta
            operacaoes = Operacao.objects.filter(id_conta=conta.id)
            extrato = getExtrato(conta)
            return Response(extrato)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

#ADMIN, CLIENT(id_client=id_client), AGENT (limited-data)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAll(request):
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #o cliente pode ver somente as contas dele
    cli = Cliente.objects.filter(id_user=user.id).first()
    if cli:
        contas = Conta.objects.filter(id_client=cli.id)
        contasSerializer = ContaSerializer(contas,many=True)
        return Response(contasSerializer.data)
    #admin pode ver todas contas
    if user.is_superuser:
        contas = Conta.objects.all()
        contasSerializer = ContaSerializer(contas,many=True)
        return Response(contasSerializer.data)
    #o agente pode ver todas contas, porem com limitacao de dados
    agent = Agente.objects.filter(id_user=user.id).first()
    if agent:
        contas = Conta.objects.all()
        contasSerializer = ContaSerializer(contas,many=True)
        refusedAtt = ['saldo', 'data_abertura']
        limited_list = []
        for a in contasSerializer.data:
            for r in refusedAtt:
                a.pop(r)
            limited_list.append(a)
        return Response(limited_list)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

#METODO CRIADO ESPECIAMENTE PARA QUESTOES DE PESQUISA E AUTO_COMPLIT
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllByNumero(request,number):
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #o cliente pode ver somente as contas dele
    cli = Cliente.objects.filter(id_user=user.id).first()
    if cli:
        contas = Conta.objects.filter(id_client=cli.id, numero__icontains=number)
        contasSerializer = ContaSerializer(contas,many=True)
        return Response(contasSerializer.data)
    #admin pode ver todas contas
    if user.is_superuser:
        contas = Conta.objects.filter(numero__icontains=number)
        contasSerializer = ContaSerializer(contas,many=True)
        return Response(contasSerializer.data)
    #o agente pode ver todas contas, porem com limitacao de dados
    agent = Agente.objects.filter(id_user=user.id).first()
    if agent:
        contas = Conta.objects.filter(numero__icontains=number)
        contasSerializer = ContaSerializer(contas,many=True)
        refusedAtt = ['saldo', 'data_abertura']
        limited_list = []
        for a in contasSerializer.data:
            for r in refusedAtt:
                a.pop(r)
            limited_list.append(a)
        return Response(limited_list)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

@transaction.atomic
def deleteConta(conta):
    conta.delete()


#CLIENT(id_client=id_client) --  nao pode apagar uma conta com saldo
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete(request,id):
    try:
        id = int(id)
    except Exception:
        return Response({"error": "Invalid id"}, status=status.HTTP_400_BAD_REQUEST)
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    cli = Cliente.objects.filter(id_user=user.id).first()
    if cli:
        conta =  Conta.objects.filter(id_client=cli.id,id=id).first()
        if conta:
            #verifica se a conta esta vazia
            if conta.saldo>0.0:
                return Response({"error": "Saldo need to be 0.0 MT"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                deleteConta(conta)
                return Response({"update":f"success"},status=status.HTTP_201_CREATED)
            except Exception:
                return Response({'error': 'unsucess'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
             
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    
        
#registrar uma conta
class Register(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Permitir acesso a apenas os que estiverem autenticados
    def post(self, request):
        user_token = request.auth
        #PEGAR O ID DO USUARIO COM ESSE TOKEN
        id_user = request.user.id
        #VERIFICAR SE O USUARIO É UM CLIENTE
        try:
            cli = Cliente.objects.get(id_user=id_user)
        except cliente.models.Cliente.DoesNotExist:
            return Response({"erro":"client not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data["id_client"] = cli.id
        data["numero"] = generate_unique_numconta(Conta.objects.all())
        data["saldo"] = 0.0
        newConta =  Temp_ContaSerializer(data=data)
        if newConta.is_valid():
            #deve salvar a conta primeiro porque, é necessário ter o id da conta para poder vincular a conta temporaria a operacção OPT
            #deste modo, o id_temp, estará vinculado a uma conta e nao a uma transferencia, deposito ou levantamento
            newc  = newConta.save()
            #Uma novo codigo codigo OPT será criado para validar essa operacao de abertura de conta
            #O id_temp nesse caso, vai ser um id da tabela temp_conta
            newOtpcode = operacaoOPTSerializer(data={
                'id_temp':newc.id,
                'optcode':generate_unique_optcode(operacaoOPT.objects.all())
            })
            if newOtpcode.is_valid():
                newOTPconta = newOtpcode.save()
            
            #envia a mensagem via OPT para o cliente
            otpmessage = mensagem_de_abertura_de_conta(newOTPconta.optcode,cli.celular,newc.data_abertura)
            send_messages(otpmessage)
            
            return Response({"message":"Quase pronto! Confirme a abertura da conta com o código que enviamos para o seu celular."},status=status.HTTP_201_CREATED)
        else:
            return Response(newConta.errors, status=status.HTTP_400_BAD_REQUEST)