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
from cliente.models import  Cliente
import cliente
from .numContaGenerator import generate_unique_numconta
from opt_module.messageGenerator import mensagem_de_abertura_de_conta
from opt_module.myOtp import send_messages
# Create your views here.

#registrar uma conta
class Register(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Permitir acesso a apenas os que estiverem autenticados
    def post(self, request):
        user_token = request.auth
        #PEGAR O ID DO USUARIO COM ESSE TOKEN
        id_user = request.user.id
        #VERIFICAR SE O USUARIO É UM CLIENTE
        try:
            cli = Cliente.objects.get(id_user=id_user)
        except cliente.models.Cliente.DoesNotExist:
            return Response({"erro":"client not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data["id_client"] = cli.id
        data["numero"] = generate_unique_numconta(Conta.objects.all())
        newConta =  Temp_ContaSerializer(data=data)
        if newConta.is_valid():
            #deve salvar a conta primeiro porque, é necessário ter o id da conta para poder vincular a conta temporaria a operacção OPT
            #deste modo, o id_temp, estará vinculado a uma conta e nao a uma transferencia, deposito ou levantamento
            newc  = newConta.save()
            #Uma novo codigo codigo OPT será criado para validar essa operacao de abertura de conta
            #O id_temp nesse caso, vai ser um id da tabela temp_conta
            newOtpcode = operacaoOPTSerializer(data={
                'id_temp':newc.id,
                'optcode':generate_unique_optcode(operacaoOPT.objects.all())
            })
            if newOtpcode.is_valid():
                newOTPconta = newOtpcode.save()
            
            #envia a mensagem via OPT para o cliente
            otpmessage = mensagem_de_abertura_de_conta(newOTPconta.optcode,cli.celular,newc.data_abertura)
            send_messages(otpmessage)
            
            return Response({"message":"Quase pronto! Confirme a abertura da conta com o código que enviamos para o seu celular."},status=status.HTTP_201_CREATED)
        else:
            return Response(newConta.errors, status=status.HTTP_400_BAD_REQUEST)