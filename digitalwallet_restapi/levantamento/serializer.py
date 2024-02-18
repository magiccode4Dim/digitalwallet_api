from rest_framework import serializers
from .models import Levantamento

class LevantamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Levantamento
        fields=('id','id_agent','id_operacao')