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