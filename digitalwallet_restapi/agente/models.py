from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Agente(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    saldo = models.FloatField(default=0.0)
    celular = models.CharField(max_length=13,default='')
    




    #DEVO FAZER METODO QUE OBRIGA O SALDO A SER ZERRO CASO A CONTA ESTEJA A SER ABERTA POR UM UTILIZADOR SIMPLES NA RUA