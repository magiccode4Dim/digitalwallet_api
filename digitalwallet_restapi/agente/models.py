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
    