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
# Create your views here.

#registrar uma conta
class Register(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Permitir acesso a apenas os que estiverem autenticados
    def post(self, request):
        user_token = request.auth
        #PEGAR O ID DO USUARIO COM ESSE TOKEN
        #VERIFICAR SE ELE É UM CLIENTE
        
        newConta =  Temp_ContaSerializer(data=request.data)
        if newConta.is_valid():
            
            
            return Response( {"token":str(user_token)})
        else:
            return Response(newConta.errors, status=status.HTTP_400_BAD_REQUEST)