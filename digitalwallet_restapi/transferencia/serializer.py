from rest_framework import serializers
from .models import Transferencia

class TransferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transferencia
        fields=('id','id_agent','id_operacao','valor','numero_conta')