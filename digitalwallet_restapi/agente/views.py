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

# Create your views here.

#DEVO COLOCAR PERMISSOES PARA A CHAMADA DE DETERMINADAS URLS
# Permitir acesso a apenas os que estiverem autenticados nao importa quem é
#Autenticacao para ver a view, significa que devo passar o token
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAll(request):
    data = Agente.objects.all()
    serializer = AgenteSerializer(data, many=True)
    return Response(serializer.data)

#Criar uma agente...
class Register(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]  # Permitir acesso a qualquer um para obtenção do token
    def post(self, request):
        #INICIALIZA OS DADOS EM UM SERIALIZADOR DA BASE DE DADOS TEMPORARIA
        newAgent = Temp_AgenteSerializer(data=request.data)
        if newAgent.is_valid():
            id_user = request.data.get('id_user')
            #deve verificar se este usuario esta associado a um usuario ou se esta associado a uma conta cliente
            try:
                user =  User.objects.get(id=id_user)
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