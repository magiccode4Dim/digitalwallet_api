from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from rest_framework.authtoken.models import Token
from .serializer import UserSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework import status
from opt_module.models import accontValidationOTP,operacaoOPT
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth.hashers import check_password

#cria um novo token para um utilizador
def recriar_token_utilizador(user):
    token = Token.objects.get(user=user)
    token.delete()
    new_token = Token.objects.create(user=user)
    return new_token

#ADMIN
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAll(request):
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #se a pessoa é superuser, entao vai receber todos os dados de todos os utilizadores
    if user.is_superuser:
        data = User.objects.all()
        serializer = UserSerializer(data, many=True)
        #remove as senhas
        users =  []
        for u in serializer.data:
            u.pop("password")
            users.append(u)
        return Response(users)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

#USER (id=id)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getMy(request):
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    if user!=None:
        serializer = UserSerializer(user, many=False)
        s = serializer.data
        s.pop("password")
        return Response(s)
    else:
        return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

#ADMIN, AGENT(limited-data), CLIENT(limited-data)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get(request,id_user_to_get):
    try:
        id_user_to_get = int(id_user_to_get)
        user_to_get = User.objects.get(id=id_user_to_get)
    except Exception as e:
        return Response({"error":"invalid id_user"},status=status.HTTP_400_BAD_REQUEST)
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    serializer = UserSerializer(user_to_get, many=False)    
    limitedData = serializer.data
    limitedData.pop("password")
    if user.is_superuser:
        #se a usuario autenticado for administrador, vai se retornar todos os dados menos a senha  
        return Response(limitedData)
    else:
        #os emails nao podem estar expostos para todos, excepto se a conta for minha
        if user_to_get.id != user.id:
            limitedData.pop("email")
        #se o usuario autenticado nao for administrador vai se retornar todos os dados menos a senha excepto quando o usuario procura é administador ou staf
        if user_to_get.is_superuser or user_to_get.is_staff:
            #nao pode permitir que clientes ou agentes vejam os perfis de administração do sistema
            return Response({"error":"invalid id_user"},status=status.HTTP_400_BAD_REQUEST)
        return Response(limitedData)

#ADMIN
#transacao para apagar um usuario
@transaction.atomic
def deleteUser(user_to_delete:User):
    user_to_delete.delete()

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete(request,id_user_to_delete):
    try:
        id_user_to_delete = int(id_user_to_delete)
        user_to_delete = User.objects.get(id=id_user_to_delete)
    except Exception as e:
        return Response({"error":"invalid id_user"},status=status.HTTP_400_BAD_REQUEST)
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    if user.is_superuser:
        try:
            deleteUser(user_to_delete=user_to_delete)
            return Response({"message":f"deleted user {id_user_to_delete}"},status=status.HTTP_202_ACCEPTED)
        except Exception:
            return Response({"error":f"failed to delete {id_user_to_delete}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"error":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

#USER (id=id)
@transaction.atomic
def updateUser(user_to_update:User):
    user_to_update.save()

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update(request):
    id_user = request.user.id
    user = User.objects.get(id=id_user)
    try:
        id = int(request.data.get('id'))
    except ValueError:
        return Response({"error": "Invalid id"}, status=status.HTTP_400_BAD_REQUEST)
    
    if id != id_user:
        return Response({"error": "Access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    
    #nao posso permitir que esses dois atributos sejam alterados
    refusedAtt = ['username', 'password']
    for att in refusedAtt:
        if att in request.data:
            return Response({"error": "invalid operation"}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            updateUser(serializer)
            return Response({"message": "Success"}, status=status.HTTP_202_ACCEPTED)
        except Exception:
            return Response({'error': 'unsucess'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#USER (id=id)
@transaction.atomic
def change_pass(user, new_password):
    user.set_password(new_password)
    user.save()
    token = recriar_token_utilizador(user)
    return token

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    id_user = request.user.id
    user = User.objects.get(id=id_user)
    #nao pode permitir a alteracao de passwords para admin ou staff
    if user.is_superuser or user.is_staff:
            return Response({"erro":"invalid iduser"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    #pega a antiga e a nova password e verifica se elas sao validas
    new_password = request.data.get('new_password')
    old_password= request.data.get('old_password')
    
    if new_password==None or old_password==None:
        return Response({"erro":"new_password and old_password is required"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    if(not check_password(old_password,user.password)):
        return Response({"erro":"invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        #se a senha é alterada, entao o token também é
        token = change_pass(user,new_password)
        return Response({"message": "Success","token":token.key}, status=status.HTTP_202_ACCEPTED)
    except Exception:
        return Response({'error': 'unsucess'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#Se as credencias forem validas, um token de sessao será retornado
class Login(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]  # Permitir acesso a qualquer um para obtenção do token

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # Autenticar o usuário
        try:
            user = authenticate(username=username, password=password)
        except Exception:
            return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_400_BAD_REQUEST)
        if user:
            try:
                #cria o token
                token = Token.objects.create(user=user)
            except IntegrityError:
                #Se o token ja existir
                token = recriar_token_utilizador(user)
                #retorna o token se ele ja existir
                #token = Token.objects.get(user=user)        
            return Response({'token': token.key},status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_400_BAD_REQUEST)

#Cadastrar novo utilizador
class Register(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]  # Permitir acesso a qualquer um para obtenção do token
    def post(self, request):
        newUser = UserSerializer(data=request.data)
        if newUser.is_valid():
            # Verificação da senha
            password = request.data.get('password')
            try:
                validate_password(password)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)          
            #GUARDA O USUARIO NAO ACTIVO
            u = newUser.save()
            return Response({'id_user':u.id},status=status.HTTP_201_CREATED)
        else:
            #retorna o motivo dos dados nao serem validos
             return Response(newUser.errors, status=status.HTTP_400_BAD_REQUEST)