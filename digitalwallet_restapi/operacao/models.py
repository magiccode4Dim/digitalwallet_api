from django.db import models
from django.contrib.auth.models import User
from conta.models import Conta
from django.utils import timezone

# Create your models here.
class Operacao(models.Model):
    id = models.AutoField(primary_key=True)
    id_conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    data_operacao = models.DateTimeField(default=timezone.now)
    valor = models.FloatField(default=0.0)