from rest_framework import serializers
from .models import Operacao

class OperacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Operacao
        fields=('id','id_conta','data_operacao')