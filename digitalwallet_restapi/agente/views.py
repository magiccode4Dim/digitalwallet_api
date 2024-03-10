from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Agente
from .serializer import AgenteSerializer
from opt_module.myOtp import send_messages
from rest_framework import status
from opt_module.messageGenerator import mensagem_de_validacao_de_conta
from opt_module.models import accontValidationOTP
from django.contrib.auth.models import User
import random
from opt_module.serializer import *
import django
import agente
from django.db import transaction
from cliente.models import Cliente
from opt_module.optcodeGenerator import generate_random_key

# Create your views here.

#DEVO COLOCAR PERMISSOES PARA A CHAMADA DE DETERMINADAS URLS
# Permitir acesso a apenas os que estiverem autenticados nao importa quem é
#Autenticacao para ver a view, significa que devo passar o token
#ADMIN, CLIENT (limited-data)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAll(request):
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #se a pessoa é superuser, entao vai receber todos os dados dos agentes
    if user.is_superuser:
        data = Agente.objects.all()
        serializer = AgenteSerializer(data, many=True)
        return Response(serializer.data)
    #se a pessoa é um cliente simples, vai receber apenas alguns dados
    client =  Cliente.objects.filter(id_user=user.id).first()
    if client!=None:
        data = Agente.objects.all()
        serializer = AgenteSerializer(data, many=True)
        limited_list =  list()
        for a in serializer.data:
            a.pop("saldo")
            a.pop("celular")
            limited_list.append(a)
        return Response(limited_list)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    
    #OS UTILIZADORES TAMBEM DEVEM TER ACESSO A LISTA DE AGENTES, PARA QUE POSSA FUNCIONAR A FUNCIONALIDADE DE AUTO_COMPLIT
    #SE FOREM UTILIZADORES SIMPLES, ELES PODERAM VER SOMENTE UMA LISTA COM O NOME E CODIGO DO AGENTE.

#retorna somente 1 agente
#ADMIN, AGENT(id==id_agent)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get(request,id_agent):
    try:
        id_agent = int(id_agent)
    except Exception as e:
        return Response({"error":"invalid id_agent"},status=status.HTTP_400_BAD_REQUEST)
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    agent = Agente.objects.filter(id_user=user.id).first()
    #verifica se a pessoa é superuser ou se se trata-se do agente que busca dados sobre a sua conta
    if not user.is_superuser and agent!=None:
        if agent.id != id_agent:
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    elif not user.is_superuser and agent==None:
        return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        data = Agente.objects.get(id=id_agent)
    except agente.models.Agente.DoesNotExist as e:
        return Response({"erro":"Not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = AgenteSerializer(data, many=False)
    return Response(serializer.data)

#verifica se o numero de telefone é valido
def IsphoneNumberValid(cell):
    #Only Mozambican Phone Number Prefix
    if cell == None:
        return False
    if cell[0:6] in ['+25882','+25883','+25884','+25885','+25886','+25887']:
        if len(cell[6:])==7:
            try:
                v = int(cell[6:])
                return True
            except ValueError:
                return False
    return False


#altera os dados de uma agente (somente o numero de telefone)
#AGENT(id==id_agent) 
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateAgenPhoneNumber(request):
    cell = request.data.get('cell')
    #Deve verificar o numero de telefone é valido... ainda é necessario escrever o metodo
    if(not IsphoneNumberValid(cell)):
        return Response({"error":"invalid invalid cell"},status=status.HTTP_400_BAD_REQUEST)
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    agent = Agente.objects.filter(id_user=user.id).first()
    #verifica se a pessoa é um agente 
    if agent==None:
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    agent.celular = cell
    agent.save()
    return Response({"update":f"new cell is {cell}"},status=status.HTTP_201_CREATED)

#recarrega a conta do agente
#ADMIN

#transacao para aumentar o saldo do agente
@transaction.atomic
def aumentarsaldoAgente(agent:Agente,valor:float):
    agent.saldo+=valor
    agent.save()
    
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def addAgentSaldo(request):
    #deve verificar se é um administrador para aumentar o saldo
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    if not user.is_superuser:
        return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    #verifica se dos dados inseridos estao correctos
    try:
        valor = float(request.data.get('valor'))
        id_agent = int(request.data.get('id_agent'))
        agent = Agente.objects.get(id=id_agent)
    except ValueError:
        return Response({"error":"invalid valor or id_agent"},status=status.HTTP_400_BAD_REQUEST)
    except TypeError:
        return Response({"error":"invalid valor or id_agent"},status=status.HTTP_400_BAD_REQUEST)
    except agente.models.Agente.DoesNotExist as e:
        return Response({"erro":"Agent Not found"}, status=status.HTTP_404_NOT_FOUND)
    try:
        aumentarsaldoAgente(agent,valor)
        return Response({"update":f"success"},status=status.HTTP_201_CREATED)
    except Exception:
        return Response({"error":"operation failed"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
#Criar uma agente...
class Register(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]  # Permitir acesso a qualquer um para obtenção do token
    def post(self, request):
        #INICIALIZA OS DADOS EM UM SERIALIZADOR DA BASE DE DADOS TEMPORARIA
        data = request.data
        data["token"] = generate_random_key([Agente.objects.all(),Temp_Agente.objects.all()])
        newAgent = Temp_AgenteSerializer(data=data)
        if newAgent.is_valid():
            id_user = request.data.get('id_user')
            cell = request.data.get('celular')
            #verifica se o numero de celular é Valido
            if(not IsphoneNumberValid(cell)):
                return Response({"error":"invalid cell"},status=status.HTTP_400_BAD_REQUEST)
            #deve verificar se este usuario esta associado a um usuario ou se esta associado a uma conta cliente
            try:
                user =  User.objects.get(id=id_user)
                #deve vericar se o usuario ja esta activado, porque nao pode permitir que este tenha 2 contas agente ou cliente
                if user.is_active:
                    return Response({"erro":"invalid iduser"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except django.contrib.auth.models.User.DoesNotExist:
                return Response({"erro":"iduser not found"}, status=status.HTTP_404_NOT_FOUND)
            #envia uma mensagem de OPT para o cliente validar a conta
            #cria um objecto accontvalidationOTP vinculado com aconta do usuario
            avOPT =  accontValidateOPTSerializer(data={
                'id_user':int(id_user),
                'optcode':generate_unique_optcode(accontValidationOTP.objects.all())
            })
            #salva o objecto (Nesse caso vai salvar primeiro em um armazenamento provisorio antes de ir a base de dados de dados validados)/ Ainda por implementar
            if avOPT.is_valid():
                avOPTob =  avOPT.save()
            else:
                return Response(avOPT.errors, status=status.HTTP_400_BAD_REQUEST)
            #cria uma mensagem opt para ser enviada ao numero que o usuario introduzio e passando o OPT gerado
            otpmessage = mensagem_de_validacao_de_conta(avOPTob.optcode,request.data.get('celular'))
            #envia a mensagem
            send_messages(otpmessage)
            #salva o agente na tabela provisoria antes de bazar para a principal
            newAgent.save()
            
             
            
            return Response({"message":"O codigo de confirmacao foi enviado ao seu contacto"},status=status.HTTP_201_CREATED)
        else:
            #retorna o motivo dos dados nao serem validos
             return Response(newAgent.errors, status=status.HTTP_400_BAD_REQUEST)