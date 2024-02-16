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
            return Response({"erro":"acess denied"}, status=status.HTTP_401_UNAUTHORIZED)
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
                    
                    
                                
            
            
        
        
