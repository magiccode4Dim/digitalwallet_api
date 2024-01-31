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

#cria um novo token para um utilizador
def recriar_token_utilizador(user):
    token = Token.objects.get(user=user)
    token.delete()
    new_token = Token.objects.create(user=user)
    return new_token

#Se as credencias forem validas, um token de sessao será retornado
class Login(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]  # Permitir acesso a qualquer um para obtenção do token

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # Autenticar o usuário
        user = authenticate(username=username, password=password)
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