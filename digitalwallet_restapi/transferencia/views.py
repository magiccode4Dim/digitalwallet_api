from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from operacao.views import userIsAgentOrClient
from rest_framework.response import Response
from rest_framework import status
from opt_module.serializer import *
from opt_module.messageGenerator import mensagem_de_confirmacao_de_transferencia
from opt_module.myOtp import send_messages
from opt_module.optcodeGenerator import generate_unique_optcode
from operacao.models import Operacao
from conta.models import Conta
from cliente.models import Cliente
from django.contrib.auth.models import User
from django.db import transaction
from deposito.models import Deposito
from transferencia.models import Transferencia
from deposito.views import operacaoIDisAlreadUsed
from agente.models import Agente
from transferencia.serializer import TransferenciaSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from operacao.models import Operacao

TAXA_DE_TRANSFERENCIA = 3.0

#ADMIN, CLIENT(id_client=id_client)
#Retorna todas as transferencias de uma determinada conta
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAll(request,id_conta):
    """
        Retorna Todos Transferências de uma determinada  Conta.</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id":int, "valor":float}...]"</br> 
            RESPONSE CODE 401: Não Autorizado.</br>
            RESPONSE CODE 404: Não Encontado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMINISTRATOR E CLIENTES</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    cli = Cliente.objects.filter(id_user=user.id).first()
    if cli:
        #pega a conta
        conta = Conta.objects.filter(id=id_conta, id_client=cli.id).first()
    #admin pode ver todas operacoes
    elif user.is_superuser:
        conta = Conta.objects.filter(id=id_conta).first()
    else:
        return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    if conta==None:
        return Response({"error":"Invalid id_conta"}, status=status.HTTP_404_NOT_FOUND)
    #pega todas as operacoes da conta
    todasOperacaos = Operacao.objects.filter(id_conta=conta.id)
    #pega todas as transferencias
    transferenciasDaConta = []
    for ops in todasOperacaos:
        t =  Transferencia.objects.filter(id_operacao=ops.id).first()
        if t:
            transferenciasDaConta.append(t)
    transSer = TransferenciaSerializer(transferenciasDaConta,many=True)
    return Response(transSer.data)
    


#TRANSACAO TRANSFERENCIA - INICIO
@transaction.atomic
def transation_Transferencia(contaOrigem,contaDestino,opera,temp_trans,otp_temp):
    if contaOrigem.saldo<(opera.valor+TAXA_DE_TRANSFERENCIA):
        #se o cliente nao tiver saldo suficiente para levantar
        raise Exception("Saldo insuficiente.")
    else:
        #o saldo sai de uma conta para outra
        contaOrigem.saldo -=(opera.valor+TAXA_DE_TRANSFERENCIA)
        contaDestino.saldo +=opera.valor
        contaOrigem.save()
        contaDestino.save()
        #registra a transferencia na tabela de transferencia da base de dados principal
        temp_trasseri = Temp_TransferenciaSerializer(temp_trans,many=False)
        trassei = TransferenciaSerializer(data=temp_trasseri.data, many=False)
        if trassei.is_valid():
            trassei.save()
        #apaga os dados residuas da base de dados temporaria
        temp_trans.delete()
        otp_temp.delete()
        
        return "Transferencia feita com sucesso!"
#TRANSACAO TRANSFERENCIA - INICIO


# Create your views here.
class Register(APIView):
    """
        Cadastra uma Transferência na Tabela Temporaria. {"id_operacao":int, "numero_conta":String..} :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 201: Criado."</br> 
            RESPONSE CODE 400: Atributo invalido.</br> 
            RESPONSE CODE 401: Não autorizado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: CLIENTES</br>  
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Permitir acesso a apenas os que estiverem autenticados
    def post(self, request):
        #verifica se o utilizador é um cliente
        id_user = request.user.id
        res = userIsAgentOrClient(id_user)
        if(not res[0]):
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
        elif(res[0] and res[1]=='agent'):
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        #pega os dados da operacao e verifica se pelomenos a operacao existe
        try:
            operac = Operacao.objects.get(id=request.data.get('id_operacao'))
        except Exception:
            return Response({"erro":"invalid id_operacao"}, status.HTTP_400_BAD_REQUEST)
        
        #verifica se o id da operacao nao esta relacionado a qualquer outra operacao de deposito, transferencia ou levantamento
        if operacaoIDisAlreadUsed(operac.id):
            return Response({"erro":"invalid id_operacao"}, status.HTTP_400_BAD_REQUEST)
        
        #verifica se o numero de conta de destino existe
        contaDestino = Conta.objects.filter(numero=request.data.get('numero_conta')).first()
        if contaDestino==None:
                return Response({"erro":"invalid numero_conta"}, status.HTTP_400_BAD_REQUEST)
            
        #verifica se a conta que o cliente quer fazer a transferencia lhe pertence
        if (res[2].id != operac.id_conta.id_client.id):
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
            
        #valida os dados enviados
        newTransferen = Temp_TransferenciaSerializer(data=request.data)
        if not newTransferen.is_valid():
            return Response(newTransferen.errors, status=status.HTTP_400_BAD_REQUEST)
        #verificar se a transferencia esta a acontecer entre contas diferentes
        if contaDestino.numero == operac.id_conta.numero:
            return Response({"erro":"invalid numero_conta"}, status.HTTP_400_BAD_REQUEST)
        #guarda a tranferencia
        newt = newTransferen.save()
        
        #nesse caso o id_temp, estara vinculado a um atributo id na tabela Transferencia
        newOtpcode = operacaoOPTSerializer(data={
                'id_temp':newt.id,
                'optcode':generate_unique_optcode(operacaoOPT.objects.all())
            })
        if newOtpcode.is_valid():
            newOTPTransferencia = newOtpcode.save()
        
        #pega os outros dados da operacao para enviar uma mensagem mais informativa ao cliente
        contCli = operac.id_conta
        client = contCli.id_client
        clientUser =  client.id_user
        donocontadestino = contaDestino.id_client.id_user
        
        otpmessage = mensagem_de_confirmacao_de_transferencia(client.celular,
                                                              clientUser.first_name+" "+clientUser.last_name,operac.valor,
                                                              contaDestino.numero,
                                                              donocontadestino.first_name+" "+donocontadestino.last_name,
                                                              operac.data_operacao,newOTPTransferencia.optcode
                                                              )
        #envia a mensagem
        send_messages(otpmessage)
        
        return Response({"message":"A mensagem de confirmação da Transferencia foi enviada para o seu contacto"}, status=status.HTTP_201_CREATED)
