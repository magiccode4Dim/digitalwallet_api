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
from operacao.views import userIsAgentOrClient
from transferencia.views import transation_Transferencia
from deposito.views import transation_Deposit
from levantamento.views import transation_Levantament
from operacao.models import Operacao
from django.db import transaction
from opt_module.messageGenerator import *
from opt_module.myOtp import send_messages
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# Create your views here.

#ADMIN
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllTempAgent(request):
    """
        Retorna Todos agentes temporários</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id":int...}...]"</br> 
            RESPONSE CODE 401: Não Autorizado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMINISTRADOR</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #se a pessoa é superuser, entao vai receber todos os dados dos agentes
    if user.is_superuser:
        data = Temp_Agente.objects.all()
        serializer = Temp_AgenteSerializer(data, many=True)
        return Response(serializer.data)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllTempClient(request):
    """
        Retorna Todos clientes temporários</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id":int...}...]"</br> 
            RESPONSE CODE 401: Não Autorizado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMINISTRADOR</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #se a pessoa é superuser, entao vai receber todos os dados dos agentes
    if user.is_superuser:
        data = Temp_Cliente.objects.all()
        serializer = Temp_ClienteSerializer(data, many=True)
        return Response(serializer.data)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllTempConta(request):
    """
        Retorna Todos Contas temporárias</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id":int...}...]"</br> 
            RESPONSE CODE 401: Não Autorizado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMINISTRADOR</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #se a pessoa é superuser, entao vai receber todos os dados dos agentes
    if user.is_superuser:
        data = Temp_Conta.objects.all()
        serializer = Temp_ContaSerializer(data, many=True)
        return Response(serializer.data)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllTempDeposito(request):
    """
        Retorna Todos Depósitostemporários</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id":int...}...]"</br> 
            RESPONSE CODE 401: Não Autorizado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMINISTRADOR</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #se a pessoa é superuser, entao vai receber todos os dados dos agentes
    if user.is_superuser:
        data = Temp_Deposito.objects.all()
        serializer = Temp_DepositoSerializer(data, many=True)
        return Response(serializer.data)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllTempLevantamento(request):
    """
        Retorna Todos Levantamentos temporários</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id":int...}...]"</br> 
            RESPONSE CODE 401: Não Autorizado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMINISTRADOR</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #se a pessoa é superuser, entao vai receber todos os dados dos agentes
    if user.is_superuser:
        data = Temp_Levantamento.objects.all()
        serializer = Temp_LevantamentoSerializer(data, many=True)
        return Response(serializer.data)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllTempTransferencia(request):
    """
        Retorna Todas Transferências temporárias</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id":int...}...]"</br> 
            RESPONSE CODE 401: Não Autorizado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMINISTRADOR</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #se a pessoa é superuser, entao vai receber todos os dados dos agentes
    if user.is_superuser:
        data = Temp_Transferencia.objects.all()
        serializer = Temp_TransferenciaSerializer(data, many=True)
        return Response(serializer.data)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAlloperacaoOPT(request):
    """
        Retorna Todos códigos OTP de operações.</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id":int...}...]"</br> 
            RESPONSE CODE 401: Não Autorizado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMINISTRADOR</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #se a pessoa é superuser, entao vai receber todos os dados dos agentes
    if user.is_superuser:
        data = operacaoOPT.objects.all()
        serializer = operacaoOPTSerializer(data, many=True)
        return Response(serializer.data)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllaccontValidationOTP(request):
    """
        Retorna Todos codigos OTP de contas por Validar.</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id":int...}...]"</br> 
            RESPONSE CODE 401: Não Autorizado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMINISTRADOR</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #se a pessoa é superuser, entao vai receber todos os dados dos agentes
    if user.is_superuser:
        data = accontValidationOTP.objects.all()
        serializer = accontValidateOPTSerializer(data, many=True)
        return Response(serializer.data)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

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
@transaction.atomic
def moveClientOrAgentetoMainDB(user,otp_temp,token):
    #Activa o usuario
    user.is_active=True
    user.save()
    #para clientes
    tempClients = Temp_Cliente.objects.filter(id_user=user.id)
    if(tempClients!=None):
        tempCliSer = Temp_ClienteSerializer(tempClients.first(),many=False)
        CliSer =  ClienteSerializer(data=tempCliSer.data, many=False)
        if CliSer.is_valid():
            CliSer.save()
            #apaga o que estiver na tabela temporaria
            tempClients.first().delete()
            #apaga o codigo otp da tabela de OPT'S, porque o codigo ja foi utilizado
            otp_temp.delete()
            return
    #para agentes
    tempAgents = Temp_Agente.objects.filter(id_user=user.id)
    if(tempAgents!=None):
        #verifica se o token que o utilizador enviou para abrir a conta agente é valido ou não
        if tempAgents.first().token != token:
            raise Exception("A Chave de activação da Conta-Agente é Invalida. Contacte o Administrador.")
        tempAgentSer = Temp_AgenteSerializer(tempAgents.first(),many=False)
        AgentSer =  AgenteSerializer(data=tempAgentSer.data, many=False)
        if AgentSer.is_valid():
            AgentSer.save()
            #apaga o que estiver na tabela temporaria
            tempAgents.first().delete()
            #apaga o codigo otp da tabela de OPT'S, porque o codigo ja foi utilizado
            otp_temp.delete()
            return
    raise Exception("we had some problem with this validation")        
    
#move a conta de um cliente para a base de dados principal
@transaction.atomic
def moveNewClientContaToMainDB(id_temp,id_client,otp_temp):
    tempContas = Temp_Conta.objects.filter(id=id_temp,id_client=id_client)
    if(tempContas!=None):
        tempContaSer =  Temp_ContaSerializer(tempContas.first(),many=False)
        contaSer = ContaSerializer(data=tempContaSer.data,many=False)
        if contaSer.is_valid():
            newc = contaSer.save()
            tempContas.first().delete()
            #apaga o otp
            otp_temp.delete()
            return newc
    raise Exception("we had some problem with this validation") 
         
        

#FUNCOES AUXILIARES - FIM

#Envio de codigo OPT para validação de uma Conta no sistema, seja ela cliente ou agente
class otp_account_validation(APIView):
    """
        Envio de OTP para validação de Conta de utilizador . {"id_user":int, "otp_code":int}. Se o utilizador a ser validado for um Agente, deve-se adicionar o atributo "Token", passando o token de cadastro :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: Validado."</br> 
            RESPONSE CODE 400: Atributo invalido.</br> 
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: NÃO</br>
        </br><b>QUEM PODE ACESSAR?</b>: TODOS</br>  
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]  # Permitir acesso a qualquer um 
    def post(self, request):
        try:
            id_user = int(request.data.get('id_user'))
            otp_code = int(request.data.get('otp_code'))
            #se o usuario que estiver a ser validado for uma gente, para além dos dados acima, vai ser receber tambem um token
            token = request.data.get('token')
        except Exception as e:
            return Response({"error":"invalid otp_code or id_user"},status=status.HTTP_400_BAD_REQUEST)
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
        
        try :
            moveClientOrAgentetoMainDB(user,otp_temp,token)#move de uma base de dados para outra
            return Response({"message":"Congrats! Your Accont is valid rigth now"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#Envio de OPT para validar um conta que o cliente criou para guardar dinheiro mesmo
class otp_client_account_validation(APIView):
    """
        Envio de OTP para validação de Conta de Cliente . { "otp_code":int} :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: Validado."</br> 
            RESPONSE CODE 400: Atributo invalido.</br>
            RESPONSE CODE 401: Acesso Negado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: CLIENTES</br>  
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Permitir acesso a apenas os que estiverem autenticados
    def post(self, request):
        #antes de mais nada, verifica se os dados sao validos
        try:
            otp_code = int(request.data.get('otp_code'))
        except Exception as e:
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
        
        #verifica se a conta que estou prestes a validar pertence ao usuario
        temp_conta = Temp_Conta.objects.get(id=otp_temp.id_temp)
        if temp_conta.id_client != cli.id:
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        #SE TUDO ESTIVER CERTO, MOVE A NOVA CONTA PARA A TABELA CERTA
        #Nesse caso, o ID_temp, fara um link com as contas que estiverem presas na tabela temporaria sem validação
        try:
            newConta = moveNewClientContaToMainDB(otp_temp.id_temp,cli.id,otp_temp)
            return Response({"message":f"Congrats! Your have new Account number is {newConta.numero}"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#Validacao de uma operacao de Deposito
class otp_deposit_validation(APIView):
    """
        Envio de OTP para validação um Depósito. { "otp_code":int} :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: Validado."</br> 
            RESPONSE CODE 400: Atributo invalido.</br>
            RESPONSE CODE 401: Acesso Negado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: AGENTES</br>  
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Permitir acesso a apenas os que estiverem autenticados
    def post(self, request):
        #Verifica se o OPT é um numero
        try:
            otp_code = int(request.data.get('otp_code'))
        except Exception as e:
            return Response({"error":"invalid otp_code"},status=status.HTTP_400_BAD_REQUEST)
        #verifica se o usuario é um agente
        id_user = request.user.id
        res = userIsAgentOrClient(id_user)
        if(not res[0]):
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
        elif(res[0] and res[1]=='client'):
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        #VERIFICA SE O CODIGO OTP ENVIADO É VALIDO
        otp_temp = operacaoOPT.objects.filter(optcode=otp_code).first()
        if(otp_temp == None):
            return Response({"error":"invalid otp_code"},status=status.HTTP_400_BAD_REQUEST)
        
        #busca o deposito temporario
        temp_depo = Temp_Deposito.objects.get(id=otp_temp.id_temp)
        
        #verifica se o agente que esta a validar o deposito é o dono do deposito
        if temp_depo.id_agent != res[2].id:
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        #busca a operacao desse deposito
        opera = Operacao.objects.get(id=temp_depo.id_operacao)
        contaCli = opera.id_conta
        
        try:
            trans_res = transation_Deposit(res[2],opera,contaCli,temp_depo,otp_temp)
            #isso significa que o deposito ocorreu com sucesso
            #DEVE MANDAR UMA MENSAGEM PARA O CLIENTE INFORMANDO SOBRE A OPERAÇÃO
            mfg = mensagem_deposito_feito_para_agente(res[2].celular,contaCli.numero,opera.valor,
                                                opera.data_operacao
                                                ,contaCli.id_client.id_user.first_name+" "+contaCli.id_client.id_user.last_name,res[2].saldo)
            send_messages(mfg)
            mfc =  mensagem_deposito_feito_para_cliente(contaCli.id_client.celular,contaCli.numero,opera.valor,
                                                        opera.data_operacao,res[2].id_user.first_name+" "+res[2].id_user.last_name,res[2].id,contaCli.saldo)
            send_messages(mfc)
            return Response({"message":f"{trans_res}"},status=status.HTTP_200_OK)
        except Exception as e:
            #quando accontece algum erro que faz com que a transacao nao seja realizada
            return Response({"error":f"{str(e)}"},status=status.HTTP_400_BAD_REQUEST)
        
#Validação de OPeração de Levantamento
class otp_levantament_validation(APIView):
    """
        Envio de OTP para validação um Levantamento. { "otp_code":int} :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: Validado."</br> 
            RESPONSE CODE 400: Atributo invalido.</br>
            RESPONSE CODE 401: Acesso Negado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: CLIENTES</br>  
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Permitir acesso a apenas os que estiverem autenticados
    def post(self, request):
        #Verifica se o OPT é um numero
        try:
            otp_code = int(request.data.get('otp_code'))
        except Exception as e:
            return Response({"error":"invalid otp_code"},status=status.HTTP_400_BAD_REQUEST)
        #verifica se o usuario é um cliente
        id_user = request.user.id
        res = userIsAgentOrClient(id_user)
        if(not res[0]):
            return Response({"erro":"acess denied"}, status=status.HTTP_401_UNAUTHORIZED)
        elif(res[0] and res[1]=='agent'):
            return Response({"erro":"acess denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        #VERIFICA SE O CODIGO OTP ENVIADO É VALIDO
        otp_temp = operacaoOPT.objects.filter(optcode=otp_code).first()
        if(otp_temp == None):
            return Response({"error":"invalid otp_code"},status=status.HTTP_400_BAD_REQUEST)
        
        #busca o levantamento temporario
        temp_levant = Temp_Levantamento.objects.get(id=otp_temp.id_temp)
        
        #busca a operacao desse levantamento
        opera = Operacao.objects.get(id=temp_levant.id_operacao)
        
        #verifica se essa operacao de levantamento que esta a ser confirmada, esta a ocorrer em uma conta que pertence ao cliente
        if opera.id_conta.id_client.id != res[2].id:
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        contaCli = opera.id_conta
        agent = Agente.objects.get(id=temp_levant.id_agent)
        
        try:
            trans_res = transation_Levantament(agent,opera,contaCli,temp_levant,otp_temp)
            #isso significa que o levantamento ocorreu com sucesso
            #DEVE MANDAR UMA MENSAGEM PARA O CLIENTE INFORMANDO SOBRE A OPERAÇÃO
            mfg =  mensagem_levantamento_feito_para_agente(agent.celular,contaCli.numero,opera.valor,opera.data_operacao,
                                                           res[2].id_user.first_name+" "+res[2].id_user.last_name,agent.saldo)
            send_messages(mfg)
            mfc = mensagem_levantamento_feito_para_cliente(res[2].celular,contaCli.numero,opera.valor,opera.data_operacao,
                                                           agent.id_user.first_name+" "+agent.id_user.last_name,agent.id,contaCli.saldo)
            send_messages(mfc)
            return Response({"message":f"{trans_res}"},status=status.HTTP_200_OK)
        except Exception as e:
            #quando accontece algum erro que faz com que a transacao nao seja realizada
            return Response({"error":f"{str(e)}"},status=status.HTTP_400_BAD_REQUEST)
        
        
#Validação de Operação de Transferencia
class otp_transferenc_validation(APIView):
    """
        Envio de OTP para validação uma Transferência. { "otp_code":int} :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: Validado."</br> 
            RESPONSE CODE 400: Atributo invalido.</br>
            RESPONSE CODE 401: Acesso Negado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: CLIENTES</br>  
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Permitir acesso a apenas os que estiverem autenticados
    def post(self, request):
        #Verifica se o OPT é um numero
        try:
            otp_code = int(request.data.get('otp_code'))
        except Exception as e:
            return Response({"error":"invalid otp_code"},status=status.HTTP_400_BAD_REQUEST)
        #verifica se o usuario é um cliente
        id_user = request.user.id
        res = userIsAgentOrClient(id_user)
        if(not res[0]):
            return Response({"erro":"acess denied"}, status=status.HTTP_401_UNAUTHORIZED)
        elif(res[0] and res[1]=='agent'):
            return Response({"erro":"acess denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        #VERIFICA SE O CODIGO OTP ENVIADO É VALIDO
        otp_temp = operacaoOPT.objects.filter(optcode=otp_code).first()
        if(otp_temp == None):
            return Response({"error":"invalid otp_code"},status=status.HTTP_400_BAD_REQUEST)
        
        
        #busca o transferecnia temporaria
        temp_transf = Temp_Transferencia.objects.get(id=otp_temp.id_temp)
        
        #busca a operacao dessa transferencia
        opera = Operacao.objects.get(id=temp_transf.id_operacao)
        
        #verifica se essa operacao de transferencia que esta a ser confirmada, esta a ocorrer em uma conta que pertence ao cliente
        if opera.id_conta.id_client.id != res[2].id:
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        #verifica se a conta de destino existe
        contaDestino = Conta.objects.filter(numero=temp_transf.numero_conta).first()
        if contaDestino==None:
            return Response({"error":"numero_conta not found"},status=status.HTTP_404_NOT_FOUND)
        
        contaCli = opera.id_conta
        
        try:
            trans_res = transation_Transferencia(contaCli,contaDestino,opera,temp_transf,otp_temp)
            #isso significa que a transferencia ocorreu com sucesso
            #DEVE MANDAR UMA MENSAGEM PARA O CLIENTE INFORMANDO SOBRE A OPERAÇÃO
            mfo = mensagem_transferencia_feita_cliente_origem(res[2].celular,opera.valor,contaDestino.numero,
                                                              contaDestino.id_client.id_user.first_name+" "+contaDestino.id_client.id_user.last_name,opera.data_operacao,
                                                              contaCli.saldo,contaCli.numero
                                                              )
            send_messages(mfo)
            mfd = mensagem_transferencia_feita_cliente_destino(contaDestino.id_client.celular,opera.valor,contaDestino.numero,
                                                               res[2].id_user.first_name+" "+res[2].id_user.last_name,opera.data_operacao,contaDestino.saldo)
            send_messages(mfd)
            return Response({"message":f"{trans_res}"},status=status.HTTP_200_OK)
        except Exception as e:
            #quando accontece algum erro que faz com que a transacao nao seja realizada
            return Response({"error":f"{str(e)}"},status=status.HTTP_400_BAD_REQUEST)
        
        
