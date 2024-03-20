from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from cliente.models import Cliente
from agente.models import Agente
from conta.models import Conta
from .serializer import OperacaoSerializer
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from operacao.models import Operacao
from deposito.models import Deposito
from deposito.serializer import DepositoSerializer
from levantamento.models import Levantamento
from levantamento.serializer import LevantamentoSerializer


#retorna todas operacoes realizadas por um determinado agente
def allOperationsAgent(agent):
    allOperations = []
    depositos_agent = Deposito.objects.filter(id_agent=agent.id)
    levantamentos_agent =  Levantamento.objects.filter(id_agent=agent.id)
    operacaoes = Operacao.objects.all()
    for op in operacaoes:
        for d in depositos_agent:
            if d.id_operacao.id==op.id:
                    allOperations.append(op)
                    break
        for l in levantamentos_agent:
            if l.id_operacao.id==op.id:
                    allOperations.append(op)
                    break
    return allOperations
    

#CLIENT(id_client=id_client),CLIENT(id_agent=id_agent)
#retorna 1 transferencia de uma operacao
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getByOperationID(request,id_operacao):
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    cli = Cliente.objects.filter(id_user=user.id).first()
    if cli:
        #pega a conta
        contas = Conta.objects.filter(id_client=cli.id)
        operacao = Operacao.objects.filter(id=id_operacao).first()
        if operacao:
            for c in contas:
                if c.id == operacao.id_conta.id:
                    #se a operacao for do cliente
                    opSer = OperacaoSerializer(operacao,many=False)
                    return Response(opSer.data)
    agent = Agente.objects.filter(id_user=user.id).first()
    if agent:
        operacao = Operacao.objects.filter(id=id_operacao).first()
        if operacao:
            #pega todos as operacoes de levantamento de deposito do agente
            allOperations = allOperationsAgent(agent)
            #verifica se para todas operacoes de levantamento e deposito, se a operacao que ele quer ver lhe pertence
            for o in allOperations:
                if o.id==operacao.id:
                    opSer = OperacaoSerializer(operacao,many=False)
                    return Response(opSer.data)
    if user.is_superuser:
        operacao = Operacao.objects.filter(id=id_operacao).first()
        if operacao:
            opSer = OperacaoSerializer(operacao,many=False)
            return Response(opSer.data)
                        
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    #DEVE CONTEMPLAR ADMINISTRADORES E AGENTES -- nesse caso so estarao permitira retornar se verificcar-se que a operacao é de levantamento ou deposito e foi feito por ele
          
#ADMIN, CLIENT(id_client=id_client),CLIENT(id_agent=id_agent)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAll(request):
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #o cliente pode ver somente as operacoes que pertencem as contas dele dele
    cli = Cliente.objects.filter(id_user=user.id).first()
    if cli:
        contas = Conta.objects.filter(id_client=cli.id)
        allOperations = []
        if contas==None:
            return Response({"error":"You don´t have contas"}, status=status.HTTP_404_NOT_FOUND)
        for c in contas:
            operacaoes = Operacao.objects.filter(id_conta=c.id)
            for o in operacaoes:
                allOperations.append(o)
        operacoesSerializer = OperacaoSerializer(allOperations,many=True)
        return Response(operacoesSerializer.data)
    #O Agente deve ver todas operacoes feitas por ele, relativas a depositos e levantamentos dele
    agent = Agente.objects.filter(id_user=user.id).first()
    if agent:
        allOperations = allOperationsAgent(agent)
        operacoesSerializer = OperacaoSerializer(allOperations,many=True)
        return Response(operacoesSerializer.data)
    #admin pode ver todas operacoes
    if user.is_superuser:
        operacaoes = Operacao.objects.all()
        operacoesSerializer = OperacaoSerializer(operacaoes,many=True)
        return Response(operacoesSerializer.data)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)


#CLIENT(id_client=id_client)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllByContID(request,id_conta):
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    cli = Cliente.objects.filter(id_user=user.id).first()
    #se for um cliente ou se for super_usuario
    if cli:
        conta = Conta.objects.filter(id_client=cli.id,id=id_conta).first()
    elif user.is_superuser:
        conta = Conta.objects.filter(id=id_conta).first()
    else:
        return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    if conta==None:
        return Response({"error":"Invalid id_conta"}, status=status.HTTP_400_BAD_REQUEST)
    operacaoes = Operacao.objects.filter(id_conta=conta.id)
    operacoesSerializer = OperacaoSerializer(operacaoes,many=True)
    return Response(operacoesSerializer.data)
#CONTEMPLAR ADMINISTRADORES E AGENTES -- nesse caso so estarao permitira retornar se verificcar-se que a operacao é de levantamento ou deposito e foi feito por ele  

def userIsAgentOrClient(id_user):
    #verifica se o usuario é um cliente
    client = Cliente.objects.filter(id_user=id_user).first()
    if(client!=None):
        return (True,'client',client)
    #Verifica se o usuario é um agente
    agent = Agente.objects.filter(id_user=id_user).first()
    if(agent!=None):
        return (True,'agent',agent)
    return (False,None,None)

# Create your views here.
class Register(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Permitir acesso a apenas os que estiverem autenticados
    def post(self, request):
        id_user = request.user.id
        #verifica se os dados enviados sao validos
        newOperacao = OperacaoSerializer(data=request.data)
        if not newOperacao.is_valid():
            return Response(newOperacao.errors, status=status.HTTP_400_BAD_REQUEST)
        #Verica se o utilizar é um cliente ou um agente
        res = userIsAgentOrClient(id_user)
        if(not res[0]):
            #se nao for nem cliente nem agente
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if(res[1]=='agent'):
                #se for ou um agente, a operacao podera ser criada sem nenhum problema
                newo = newOperacao.save()
                return Response({"id_operacao":newo.id}, status=status.HTTP_201_CREATED)
            elif(res[1]=='client'):
                #se for um cliente, o numero de conta da operacao, deve pertencer a uma das contas dele
                try: 
                    Conta.objects.get(id=request.data.get('id_conta'),id_client=res[2].id)
                    newo = newOperacao.save()
                    return Response({"id_operacao":newo.id}, status=status.HTTP_201_CREATED)
                except Exception as e:
                     #quando a pessoa esta tentar criar uma operacao com uma conta que nao lhe pertence
                     return Response({"erro":"invalid numero conta"}, status=status.HTTP_401_UNAUTHORIZED)
                    
                    
                                
            
            
        
        
