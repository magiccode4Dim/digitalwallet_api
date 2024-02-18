from rest_framework import serializers
from .models import Transferencia

class TransferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transferencia
        fields=('id','id_operacao','numero_conta')