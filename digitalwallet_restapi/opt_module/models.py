from django.db import models
from django.contrib.auth.models import User
from operacao.models import Operacao
from .optcodeGenerator import *
# Create your models here.

#Classe que armazena codigos OPT para validacao de operacoes como deposito, transferencia e levantamente
class operacaoOPT(models.Model):
    id = models.AutoField(primary_key=True)
    id_operacao = models.ForeignKey(Operacao, on_delete=models.CASCADE)
    optcode = models.IntegerField(unique=True)
            
#Classe OPT para validacao de contas
class accontValidationOTP(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    optcode = models.IntegerField(unique=True)


#NESSES OBJECTOS OPT, FALTA ADICIONAR DATA DE CRIACAO E MECANISMO DE EXPIRACAO E INVALIDACAO