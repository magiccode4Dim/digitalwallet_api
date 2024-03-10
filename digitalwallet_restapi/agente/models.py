from django.db import models
from django.contrib.auth.models import User
import random
# Create your models here.
class Agente(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    saldo = models.FloatField(default=0.0)
    celular = models.CharField(max_length=13,default='')
    token = models.CharField(max_length=45,unique=True)
    
    #deve ser acrescentado um campo, relativo ao codigo que sera fornecido exclusivamente ao agente
    #no ambito da abertura da sua conta na loja. Neste contexto, ao validar uma conta agente,
    # o agente nao so tera que passar o codigo otp como tambem tera que introduzir o token indicado pelo administrador do
    #sistema
    




    #DEVO FAZER METODO QUE OBRIGA O SALDO A SER ZERRO CASO A CONTA ESTEJA A SER ABERTA POR UM UTILIZADOR SIMPLES NA RUA