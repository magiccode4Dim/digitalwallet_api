from django.db import models
from django.contrib.auth.models import User
from cliente.models import Cliente
from django.utils import timezone

# Create your models here.
class Conta(models.Model):
    id = models.AutoField(primary_key=True)
    id_client = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    numero = models.CharField(max_length=100)
    data_abertura = models.DateTimeField(default=timezone.now)
    saldo = models.FloatField(default=0.0)
    
