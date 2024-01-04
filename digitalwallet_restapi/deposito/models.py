from django.db import models
from django.contrib.auth.models import User
from agente.models import Agente
from operacao.models import Operacao

# Create your models here.
class Deposito(models.Model):
    id = models.AutoField(primary_key=True)
    id_agent = models.ForeignKey(Agente, on_delete=models.CASCADE)
    id_operacao = models.ForeignKey(Operacao, on_delete=models.CASCADE)
    valor = models.FloatField()