from rest_framework import serializers
from .models import Agente

class AgenteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Agente
        fields=('id','id_user','saldo','celular','token')