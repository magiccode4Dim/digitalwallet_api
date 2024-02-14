from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from .messageGenerator import mensagem_de_validacao_de_conta
from .myOtp import send_messages
from agente.models import Agente
from cliente.models import Cliente
from agente.serializer import AgenteSerializer
from cliente.serializer import ClienteSerializer
import cliente
import django
from conta.serializer import *
from conta.models import *
# Create your views here.

#FUNCOES AUXILIARES - INICIO

#Retorna o numero de celular
def getTempUserPhoneNumber(id_user):
    #verifica se o usuario é um cliente
    tempClient = Temp_Cliente.objects.filter(id_user=id_user).first()
    if(tempClient!=None):
        return tempClient.celular
    #Verifica se o usuario é um agente
    tempAgent = Temp_Agente.objects.filter(id_user=id_user).first()
    if(tempAgent!=None):
        return tempAgent.celular
    return None

#Move dados das tabelaS Temporarias Agente ou Cliente
def moveClientOrAgentetoMainDB(user):
    #para clientes
    tempClients = Temp_Cliente.objects.filter(id_user=user.id)
    if(tempClients!=None):
        tempCliSer = Temp_ClienteSerializer(tempClients.first(),many=False)
        CliSer =  ClienteSerializer(data=tempCliSer.data, many=False)
        if CliSer.is_valid():
            CliSer.save()
            #apaga o que estiver na tabela temporaria
            tempClients.first().delete()
            return True
    #para agentes
    tempAgents = Temp_Agente.objects.filter(id_user=user.id)
    if(tempAgents!=None):
        tempAgentSer = Temp_AgenteSerializer(tempAgents.first(),many=False)
        AgentSer =  AgenteSerializer(data=tempAgentSer.data, many=False)
        if AgentSer.is_valid():
            AgentSer.save()
            #apaga o que estiver na tabela temporaria
            tempAgents.first().delete()
            return True
    return False        
    
#move a conta de um cliente para a base de dados principal
def moveNewClientContaToMainDB(id_temp,id_client):
    tempContas = Temp_Conta.objects.filter(id=id_temp,id_client=id_client)
    if(tempContas!=None):
        tempContaSer =  Temp_ContaSerializer(tempContas.first(),many=False)
        contaSer = ContaSerializer(data=tempContaSer.data,many=False)
        if contaSer.is_valid():
            newc = contaSer.save()
            tempContas.first().delete()
            return newc
    return None
         
        

#FUNCOES AUXILIARES - FIM

#Envio de codigo OPT para validação de uma Conta no sistema, seja ela cliente ou agente
class otp_account_validation(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]  # Permitir acesso a qualquer um 
    def post(self, request):
        try:
            id_user = int(request.data.get('id_user'))
            otp_code = int(request.data.get('otp_code'))
        except ValueError as e:
            return Response({"error":"invalid otp_code"},status=status.HTTP_400_BAD_REQUEST)
        #Verificar se opt existe
        otp_temp = accontValidationOTP.objects.filter(id_user=id_user,optcode=otp_code).first()
        try:
            user =  User.objects.get(id=id_user)
        except django.contrib.auth.models.User.DoesNotExist:
            return Response({"error":"invalid id_user"},status=status.HTTP_400_BAD_REQUEST)
        if(otp_temp == None):
            #se o codigo OPT  nao existir, verifica se o usuario que se pretende validar existe
            if user != None:
                #caso ele exista, verifica se ele esta desativado. Caso esteja desativado, envia de novo o codigo OPT
                if( not user.is_active):
                    #apaga o antigo codigo opt do usuario, se existir, criar um novo opt e reenvia
                    otp_old= accontValidationOTP.objects.filter(id_user=id_user).first()
                    if(otp_old!=None):
                        otp_old.delete()
                    #busca o numero de celular do cliente
                    cell = getTempUserPhoneNumber(id_user)
                    if(cell==None):
                        #quer dizer que a pessoa esta a tentar validar uma conta de um usuario que nao é nem cliente nem agente
                        #assim sendo, a conta deve ser apagada
                        user.delete()
                        return Response({"error":"invalid OPT,this client or agent does not exist. Please create new account"},status=status.HTTP_400_BAD_REQUEST)
                        
                    #cria um novo codigo OTP e reenvia
                    avOPT = accontValidationOTP(id_user=id_user,optcode=generate_unique_optcode(accontValidationOTP.objects.all()))
                    avOPT.save()
                    otpmessage = mensagem_de_validacao_de_conta(avOPT.optcode,cell)
                    #envia uma nova mensagem OPT
                    send_messages(otpmessage)
                    return Response({"error":"invalid OPT, we sent you new OPT code"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    #caso a pessoa esteja a tentar validar o codigo OPT de um usuario que ja existe
                    return Response({"error":"invalid id_user"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":"invalid opt data"},status=status.HTTP_400_BAD_REQUEST)
        #Se o codigo OTP existir, o codigo vai continuar a execução por aqui
        #este techo do codigo vai executar se o codigo for valido
        #a conta vai ser activada e os dados da tabela temporaria irao para a tabela definitiva
        user.is_active=True
        user.save()
        if (moveClientOrAgentetoMainDB(user)):#move de uma base de dados para outra
            #apaga o codigo otp da tabela de OPT'S, porque o codigo ja foi utilizado
            otp_temp.delete()
            return Response({"message":"Congrats! Your Accont is valid rigth now"},status=status.HTTP_200_OK)
        else:
            return Response({"error":"we had some problem with this validation"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#Envio de OPT para validar um conta que o cliente criou para guardar dinheiro mesmo
class otp_client_account_validation(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Permitir acesso a apenas os que estiverem autenticados
    def post(self, request):
        #antes de mais nada, verifica se os dados sao validos
        try:
            otp_code = int(request.data.get('otp_code'))
        except ValueError as e:
            return Response({"error":"invalid otp_code"},status=status.HTTP_400_BAD_REQUEST)
        
        id_user = request.user.id
        #VERIFICAR SE O USUARIO É UM CLIENTE PORQUE, SO PODEM VALIDAR CONTAS DE DINHEIRO AQUELES QUE SÃO CLIENTE
        try:
            cli = Cliente.objects.get(id_user=id_user)
        except cliente.models.Cliente.DoesNotExist:
            return Response({"erro":"client not found"}, status=status.HTTP_404_NOT_FOUND)
        
        #VERIFICA SE O CODIGO OTP ENVIADO É VALIDO
        otp_temp = operacaoOPT.objects.filter(optcode=otp_code).first()
        if(otp_temp == None):
            #Se nao for valido, não há como, o utilizador terá que abrir a conta novamente
            return Response({"error":"invalid otp_code"},status=status.HTTP_400_BAD_REQUEST)
        
        #SE TUDO ESTIVER CERTO, MOVE A NOVA CONTA PARA A TABELA CERTA
        #Nesse caso, o ID_temp, fara um link com as contas que estiverem presas na tabela temporaria sem validação
        newConta = moveNewClientContaToMainDB(otp_temp.id_temp,cli.id)
        if(newConta!=None):
            #apaga o otp
            otp_temp.delete()
            return Response({"message":f"Congrats! Your have new Account number is {newConta.numero}"},status=status.HTTP_200_OK)
        else:
            return Response({"error":"we had some problem with this validation"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        