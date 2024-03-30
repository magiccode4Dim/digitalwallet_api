from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from opt_module.serializer import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from opt_module.messageGenerator import mensagem_de_validacao_de_conta
from opt_module.myOtp import send_messages
import django
from agente.views import IsphoneNumberValid
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Cliente
from .serializer  import ClienteSerializer
from agente.models import Agente
import cliente


#ADMIN, AGENT (limited-data)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAll(request):
    """
        Retorna todos Clientes :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id": int,"id_user": int,"saldo": float,"celular"...}..]"</br>  
            RESPONSE CODE 401: Acesso Negado.</br> 
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMINISTRADOR E AGENTES</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #se a pessoa é superuser, entao vai receber todos os dados dos agentes
    if user.is_superuser:
        data = Cliente.objects.all()
        serializer = ClienteSerializer(data, many=True)
        return Response(serializer.data)
    #se a pessoa é um AGENTE simples, vai receber apenas alguns dados
    agent =  Agente.objects.filter(id_user=user.id).first()
    if agent!=None:
        data = Cliente.objects.all()
        serializer = ClienteSerializer(data, many=True)
        limited_list =  list()
        #dados que nao devem ser expostos
        refusedAtt = ['celular']
        for a in serializer.data:
            for r in refusedAtt:
                a.pop(r)
            limited_list.append(a)
        return Response(limited_list)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

#retorna somente 1 cliente
#CLIENT(id==id_client) 
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getMy(request):
    """
        Retorna os dados do Cliente Autenticado :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: {"id": int,"id_user": int,"saldo": float,"celular"...}"</br>  
            RESPONSE CODE 401: Acesso Negado.</br> 
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: CLIENTES</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    client = Cliente.objects.filter(id_user=user.id).first()
    if client!=None:
        serializer = ClienteSerializer(client, many=False)
        return Response(serializer.data)
    else:
        return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

#ADMIN, AGENT(limited-data), CLIENT(id==id_client) 
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get(request,id_client):
    """
        Retorna o Cliente com o Id :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: {"id": int,"id_user": int,"saldo": float,"celular"...}"</br>
            RESPONSE CODE 400: Parametro Invalido.</br>
            RESPONSE CODE 401: Acesso Negado.</br>
            RESPONSE CODE 404: Não Encontrado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: TODOS</br>  
    """
    agent =  None
    try:
        id_client = int(id_client)
    except Exception as e:
        return Response({"error":"invalid id_client"},status=status.HTTP_400_BAD_REQUEST)
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    client = Cliente.objects.filter(id_user=user.id).first()
    #verifica se a pessoa é superuser ou se se trata-se do cliente que busca dados sobre a sua conta
    if not user.is_superuser and  client!=None:
        if client.id != id_client:
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    elif not user.is_superuser and client==None:
        #Verifica-se se a pessoa é um agente
        agent = Agente.objects.filter(id_user=user.id).first()
        if agent == None:
            #se  pessoa não for um agente
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        data = Cliente.objects.get(id=id_client)
    except cliente.models.Cliente.DoesNotExist as e:
        return Response({"erro":"Not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ClienteSerializer(data, many=False)
    if agent!=None:
        #retorna dados limitados
        limitedData = serializer.data
        #atributos que nao devem ser expostos
        refusedAtt = ['celular']
        for r in refusedAtt:
            limitedData.pop(r)
        return Response(limitedData)
    else:
        return Response(serializer.data)

#transacao para actualizar dados de agentes
@transaction.atomic
def updateClient(cli):
    cli.save()

#altera os dados de uma agente (somente o numero de telefone)
#CLIENT(id==id_client) 
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update(request):
    """
        Actualiza os dados do a Cliente Autenticado : {"celular":..}</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 201: Actualizado com Sucesso.</br>
            RESPONSE CODE 400: Parâmetros invalidos.</br>
            RESPONSE CODE 401: Acesso Negado.</br> 
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: CLIENTES</br>  
    """
    #identificacao
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    cli = Cliente.objects.filter(id_user=user.id).first()
    if cli==None:
        return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    #verificacao de dados da requisicao
    try:
        id_client = int(request.data.get('id'))
    except Exception:
        return Response({"error": "Invalid id"}, status=status.HTTP_400_BAD_REQUEST)
    if id_client!=cli.id:
        return Response({"error": "Access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    cell = request.data.get('celular')
    #Deve verificar o numero de telefone é valido... ainda é necessario escrever o metodo
    if cell!=None:
        if(not IsphoneNumberValid(cell)):
            return Response({"error":"invalid celular"},status=status.HTTP_400_BAD_REQUEST)
    
    #nao permitir que alguns atributos sejam alguns atributos sejam alterados
    refusedAtt = ['id_user']
    for att in refusedAtt:
        if att in request.data:
            return Response({"error": "invalid operation"}, status=status.HTTP_400_BAD_REQUEST)
        
    #salvar
    serializer = ClienteSerializer(cli, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            updateClient(serializer)
            return Response({"message": "Success"}, status=status.HTTP_202_ACCEPTED)
        except Exception:
            return Response({'error': 'unsucess'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
#Criar uma conta cliente...
class Register(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]  # Permitir acesso a qualquer um para obtenção do token
    def post(self, request):
        #INICIALIZA OS DADOS EM UM SERIALIZADOR DA BASE DE DADOS TEMPORARIA
        newClient = Temp_ClienteSerializer(data=request.data)
        if newClient.is_valid():
            id_user = request.data.get('id_user')
            cell = request.data.get('celular')
            #verifica se o numero de celular é Valido
            if(not IsphoneNumberValid(cell)):
                return Response({"error":"invalid invalid cell"},status=status.HTTP_400_BAD_REQUEST)
            try:
                user =  User.objects.get(id=id_user)
                if user.is_active:
                    return Response({"erro":"invalid iduser"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                #verifica se o usuario é um administrador, porque administradores nao podem ter contas cliente ou agente
                if user.is_superuser or user.is_staff:
                    return Response({"erro":"invalid iduser"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except django.contrib.auth.models.User.DoesNotExist:
                return Response({"erro":"iduser not found"}, status=status.HTTP_404_NOT_FOUND)
            avOPT =  accontValidateOPTSerializer(data={
                'id_user':int(id_user),
                'optcode':generate_unique_optcode(accontValidationOTP.objects.all())
            })
            if avOPT.is_valid():
                avOPTob =  avOPT.save()
            else:
                return Response(avOPT.errors, status=status.HTTP_400_BAD_REQUEST)
            otpmessage = mensagem_de_validacao_de_conta(avOPTob.optcode,request.data.get('celular'))
            #envia a mensagem
            send_messages(otpmessage)
            newClient.save()
 
            return Response({'username':user.username,"message":"O codigo de confirmacao foi enviado ao seu contacto"},status=status.HTTP_201_CREATED)
        else:
            #retorna o motivo dos dados nao serem validos
             return Response(newClient.errors, status=status.HTTP_400_BAD_REQUEST)

