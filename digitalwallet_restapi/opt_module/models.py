from django.db import models
from .optcodeGenerator import *
from django.utils import timezone
# Create your models here.

#Classe que armazena codigos OPT para validacao de operacoes como deposito, transferencia e levantamente
class operacaoOPT(models.Model):
    id = models.AutoField(primary_key=True)
    optcode = models.IntegerField(unique=True)
    #id_temp é o ID do objecto temporario associado a essa validacao OTP. nesse caso o objecto temporario é uma operacao
    id_temp = models.IntegerField()
            
#Classe OPT para validacao de contas
#Quando a conta é criada, ela já fica desabilitada. É habilitada somente quando esse OTP for confirmado
class accontValidationOTP(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.IntegerField(unique=True)
    optcode = models.IntegerField(unique=True)
    
#NESSES OBJECTOS OPT, FALTA ADICIONAR DATA DE CRIACAO E MECANISMO DE EXPIRACAO E INVALIDACAO

#COPIA DOS MODELOS PARA ARMAZENAMENTO TEMPORARIO

#NOTA IMPORTANTE :
"""
Para que haja mais performance no sistema, 
é melhor que existam duas base de dadOs....

MAIS DETALHES SOBRE ISSO, ENCONTRAM-SE DESCRITOS NO FICHEIRO como_fazer_o_migrate.txt


"""
#Modelo para armazenamento de agentes temporarios cuja validacao ainda nao foi realizada via OTP
class Temp_Agente(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.IntegerField(unique=True)
    saldo = models.FloatField(default=0.0)
    celular = models.CharField(max_length=13,default='')

class Temp_Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.IntegerField(unique=True)
    celular = models.CharField(max_length=13,default='')
    
class Temp_Conta(models.Model):
    id = models.AutoField(primary_key=True)
    id_client =  models.IntegerField()
    numero = models.CharField(max_length=100,unique=True)
    data_abertura = models.DateTimeField(default=timezone.now)
    saldo = models.FloatField(default=0.0)

class Temp_Deposito(models.Model):
    id = models.AutoField(primary_key=True)
    id_agent = models.IntegerField(default=0)
    id_operacao = models.IntegerField(unique=True)
    
class Temp_Levantamento(models.Model):
    id = models.AutoField(primary_key=True)
    id_agent = models.IntegerField()
    id_operacao = models.IntegerField(unique=True)
    
class Temp_Transferencia(models.Model):
    id = models.AutoField(primary_key=True)
    id_operacao = models.IntegerField(unique=True)
    numero_conta = models.CharField(max_length=100)