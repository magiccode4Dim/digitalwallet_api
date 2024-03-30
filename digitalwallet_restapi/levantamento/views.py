from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from operacao.views import userIsAgentOrClient
from rest_framework.response import Response
from rest_framework import status
from opt_module.serializer import *
from opt_module.messageGenerator import mensagem_de_confirmacao_de_levantamento
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
from .serializer import LevantamentoSerializer
from opt_module.serializer import Temp_DepositoSerializer
from deposito.views import operacaoIDisAlreadUsed
from agente.models import Agente
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

TAXA_DE_LEVANTAMENTO = 2.0

#AGENT(id_agent=id_agent)
#Retorna todas as levantamentos
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllAgent(request):
    """
        Retorna Todos Levantamentos de um determinado Agente :</br>
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
        levantamentos = Levantamento.objects.filter(id_agent=agent.id)
        levSer = LevantamentoSerializer(levantamentos,many=True)
        return Response(levSer.data)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

#ADMIN, CLIENT(id_client=id_client)
#Retorna todas as levantamentos de uma determinada conta
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAll(request,id_conta):
    """
        Retorna Todos Levantamentos da conta com o ID :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id":int, "valor":float}...]"</br> 
            RESPONSE CODE 401: Não Autorizado.</br>
            RESPONSE CODE 404: Não encontrado.</br>
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
    levantamentosDaConta = []
    for ops in todasOperacaos:
        l =  Levantamento.objects.filter(id_operacao=ops.id).first()
        if l:
            levantamentosDaConta.append(l)
    levSer = LevantamentoSerializer(levantamentosDaConta,many=True)
    return Response(levSer.data)
    

#TRANSACAO LEVANTAMENTO - INICIO
@transaction.atomic
def transation_Levantament(agent,opera,conta,temp_leva,otp_temp):
    if conta.saldo<(opera.valor+TAXA_DE_LEVANTAMENTO):
        #se o cliente nao tiver saldo suficiente para levantar
        raise Exception("Saldo insuficiente.")
    else:
        #o saldo sai da conta do cliente e vai para o agente
        conta.saldo -=(opera.valor+TAXA_DE_LEVANTAMENTO)
        agent.saldo +=opera.valor
        conta.save()
        agent.save()
        #registra o levantamento na tabela de levantamentos da base de dados principal
        temp_levseri = Temp_LevantamentoSerializer(temp_leva,many=False)
        levsei = LevantamentoSerializer(data=temp_levseri.data, many=False)
        if levsei.is_valid():
            levsei.save()
        #apaga os dados residuas da base de dados temporaria
        temp_leva.delete()
        otp_temp.delete()
        
        return "Levantamento feito com sucesso!"
#TRANSACAO LEVANTAMENTO - INICIO



# Create your views here.
class Register(APIView):
    """
        Cadastra um Levantamento na Tabela Temporaria. {"id_operacao":int, "valor":float...} :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 201: Criado."</br> 
            RESPONSE CODE 400: Atributo invalido.</br> 
            RESPONSE CODE 401: Não autorizado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: CLIENTES</br>  
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Permitir acesso a apenas os que estiverem autenticados
    def post(self, request):
        #verifica se o utilizador é um cliente
        id_user = request.user.id
        res = userIsAgentOrClient(id_user)
        if(not res[0]):
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
        elif(res[0] and res[1]=='agent'):
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        #pega os dados da operacao e verifica se pelomenos a operacao existe
        try:
            operac = Operacao.objects.get(id=request.data.get('id_operacao'))
        except Exception:
            return Response({"erro":"invalid id_operacao"}, status.HTTP_400_BAD_REQUEST)
        #verifica se id do agente existe
        try:
            agent = Agente.objects.get(id=request.data.get('id_agent'))
        except Exception:
            return Response({"erro":"invalid id_agent"}, status.HTTP_400_BAD_REQUEST)
        
        #verifica se o id da operacao nao esta relacionado a qualquer outra operacao de deposito, transferencia ou levantamento
        if operacaoIDisAlreadUsed(operac.id):
            return Response({"erro":"invalid id_operacao"}, status.HTTP_400_BAD_REQUEST)
        
        #verifica se a conta que o cliente quer fazer o levantamento lhe pertence
        if (res[2].id != operac.id_conta.id_client.id):
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
            
        #valida os dados enviados
        newLevant = Temp_LevantamentoSerializer(data=request.data)
        if not newLevant.is_valid():
            return Response(newLevant.errors, status=status.HTTP_400_BAD_REQUEST)
        #guarda o Levantamento
        newl = newLevant.save()
        
        #nesse caso o id_temp, estara vinculado a um atributo id na tabela Levantamento
        newOtpcode = operacaoOPTSerializer(data={
                'id_temp':newl.id,
                'optcode':generate_unique_optcode(operacaoOPT.objects.all())
            })
        if newOtpcode.is_valid():
            newOTPDeposito = newOtpcode.save()
        
        #pega os outros dados da operacao para enviar uma mensagem mais informativa ao cliente
        contCli = operac.id_conta
        client = contCli.id_client
        clientUser =  client.id_user
        
        
        otpmessage = mensagem_de_confirmacao_de_levantamento(client.celular,
                                                             clientUser.first_name+" "+clientUser.last_name,
                                                             agent.id_user.first_name+" "+agent.id_user.last_name,
                                                             agent.id,operac.valor,contCli.numero,
                                                             operac.data_operacao,newOTPDeposito.optcode)
        #envia a mensagem
        send_messages(otpmessage)
        
        return Response({"message":"A mensagem de confirmação do Levantamento foi enviada para o seu contacto"}, status=status.HTTP_201_CREATED)
