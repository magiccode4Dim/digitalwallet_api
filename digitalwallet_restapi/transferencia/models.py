from django.db import models
from django.contrib.auth.models import User
from agente.models import Agente
from operacao.models import Operacao

# Create your models here.
class Transferencia(models.Model):
    id = models.AutoField(primary_key=True)
    id_operacao = models.OneToOneField(Operacao, on_delete=models.CASCADE)
    numero_conta = models.CharField(max_length=100)
    
