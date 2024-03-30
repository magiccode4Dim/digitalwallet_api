from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from operacao.views import userIsAgentOrClient
from rest_framework.response import Response
from rest_framework import status
from opt_module.serializer import *
from opt_module.messageGenerator import mensagem_de_confirmacao_de_deposito
from opt_module.myOtp import send_messages
from opt_module.optcodeGenerator import generate_unique_optcode
from operacao.models import Operacao
from conta.models import Conta
from cliente.models import Cliente
from django.contrib.auth.models import User
from django.db import transaction
from deposito.models import Deposito
from transferencia.models import Transferencia
from levantamento.models import Levantamento
from .serializer import DepositoSerializer
from opt_module.serializer import Temp_DepositoSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from agente.models import Agente

#AGENT(id_agent=id_agent)
#Retorna todos depositos
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllAgent(request):
    """
        Retorna Todos os Depósitos de um determinado Agente :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id":int, "valor":float}...]"</br> 
            RESPONSE CODE 401: Não Autorizado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: AGENTES</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    agent = Agente.objects.filter(id_user=user.id).first()
    if agent:
        depositos = Deposito.objects.filter(id_agent=agent.id)
        depSer = DepositoSerializer(depositos,many=True)
        return Response(depSer.data)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

#ADMIN, CLIENT(id_client=id_client)
#Retorna todas os depositos de uma determinada conta
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAll(request,id_conta):
    """
        Retorna depositos de uma determinada conta.</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id": int,"data_deposito": "String","valor": float..}...]"</br>  
            RESPONSE CODE 401: Acesso Negado.</br>
            RESPONSE CODE 404: Não Encontrado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMINISTRADOR E CLIENTES</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    cli = Cliente.objects.filter(id_user=user.id).first()
    if cli:
        #pega a conta
        conta = Conta.objects.filter(id=id_conta, id_client=cli.id).first()
    #admin pode ver todas operacoes
    elif user.is_superuser:
        conta = Conta.objects.filter(id=id_conta).first()
    else:
        return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    if conta==None:
        return Response({"error":"Invalid id_conta"}, status=status.HTTP_404_NOT_FOUND)
    #pega todas as operacoes da conta
    todasOperacaos = Operacao.objects.filter(id_conta=conta.id)
    #pega todas as transferencias
    depositosDaConta = []
    for ops in todasOperacaos:
        d =  Deposito.objects.filter(id_operacao=ops.id).first()
        if d:
            depositosDaConta.append(d)
    depSer = DepositoSerializer(depositosDaConta,many=True)
    return Response(depSer.data)
    

#TRANSACAO DEPOSITO - INICIO
@transaction.atomic
def transation_Deposit(agent,opera,conta,temp_depo,otp_temp):
    if agent.saldo<opera.valor:
        #se o agente nao tiver saldo suficiente para depositar na conta do cliente
        raise Exception("Saldo insuficiente.")
    else:
        #o saldo sai da conta do agente e vai para a conta do cliente
        agent.saldo -=opera.valor
        conta.saldo +=opera.valor 
        agent.save()
        conta.save()
        #registra o deposito na tabela de depositos da base de dados principal
        temp_depseri = Temp_DepositoSerializer(temp_depo,many=False)
        depsei = DepositoSerializer(data=temp_depseri.data, many=False)
        if depsei.is_valid():
            depsei.save()
        #apaga os dados residuas da base de dados temporaria
        temp_depo.delete()
        otp_temp.delete()
        
        return "Deposito feito com sucesso!"
#TRANSACAO DEPOSITO - INICIO

#verifica se o ID da operacao ja foi usado alguma vez
def operacaoIDisAlreadUsed(id_operacao):
    if (Deposito.objects.filter(id_operacao=id_operacao)==None):
        return True
    if (Levantamento.objects.filter(id_operacao=id_operacao)==None):
        return True
    if (Transferencia.objects.filter(id_operacao=id_operacao)==None):
        return True
    return False



# Create your views here.
class Register(APIView):
    """
        Cadastra um Deposito na Tabela Temporaria. {"id_operacao":int, "id_agent":int} :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 201: Criado."</br> 
            RESPONSE CODE 400: Atributo invalido.</br> 
            RESPONSE CODE 401: Não autorizado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: TODOS</br>  
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Permitir acesso a apenas os que estiverem autenticados
    def post(self, request):
        #verifica se o utilizador é um agente
        id_user = request.user.id
        res = userIsAgentOrClient(id_user)
        if(not res[0]):
            return Response({"erro":"acess denied"}, status=status.HTTP_401_UNAUTHORIZED)
        elif(res[0] and res[1]=='client'):
            return Response({"erro":"acess denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        #pega os dados da operacao e verifica se pelomenos a operacao existe
        try:
            operac = Operacao.objects.get(id=request.data.get('id_operacao'))
        except Exception:
            return Response({"erro":"invalid id_operacao"}, status.HTTP_400_BAD_REQUEST)
        
        #verifica se o id da operacao nao esta relacionado a qualquer outra operacao de deposito, transferencia ou levantamento
        if operacaoIDisAlreadUsed(operac.id):
            return Response({"erro":"invalid id_operacao"}, status.HTTP_400_BAD_REQUEST)
        
        #valida os dados enviados
        newDepos = Temp_DepositoSerializer(data=request.data)
        if not newDepos.is_valid():
            return Response(newDepos.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        #muda o id do agente com o id obtido atravez do token de quem fez a requisicao
        newd = newDepos.save()
        newd.id_agent = res[2].id
        newd.save()
        
        #nesse caso o id_temp, estara vinculado a um atributo na tabela Deposito
        newOtpcode = operacaoOPTSerializer(data={
                'id_temp':newd.id,
                'optcode':generate_unique_optcode(operacaoOPT.objects.all())
            })
        if newOtpcode.is_valid():
            newOTPDeposito = newOtpcode.save()
        
        #pega os outros dados da operacao para enviar uma mensagem mais informativa ao agente
        contCli = operac.id_conta
        client = contCli.id_client
        clientUser =  client.id_user
        
        otpmessage = mensagem_de_confirmacao_de_deposito(newOTPDeposito.optcode,res[2].celular,contCli.numero,operac.valor,operac.data_operacao,clientUser.first_name+" "+clientUser.last_name)
        #envia a mensagem
        send_messages(otpmessage)
        
        return Response({"message":"A mensagem de confirmação de Deposito foi enviada para o seu contacto"}, status=status.HTTP_201_CREATED)
        
        
        
