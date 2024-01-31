from .models import *
from rest_framework import serializers
from .optcodeGenerator import generate_unique_optcode

class operacaoOPTSerializer(serializers.ModelSerializer):
    class Meta:
        model = operacaoOPT
        fields = ('id', 'id_operacao','optcode')
    def create(self, validated_data):
        # Cria o usuário sem definir a senha ainda
        operacaootpcode = operacaoOPT.objects.create(**validated_data)
        operacaootpcode.save()

        return operacaootpcode

class accontValidateOPTSerializer(serializers.ModelSerializer):
    class Meta:
        model =  accontValidationOTP
        fields = ('id', 'id_user','optcode')
    def create(self, validated_data):
        # Cria o usuário sem definir a senha ainda
        accontotpcode = accontValidationOTP.objects.create(**validated_data)
        accontotpcode.save()

        return accontotpcode

