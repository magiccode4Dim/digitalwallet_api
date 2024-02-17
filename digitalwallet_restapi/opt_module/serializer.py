from .models import *
from rest_framework import serializers
from .optcodeGenerator import generate_unique_optcode

class operacaoOPTSerializer(serializers.ModelSerializer):
    class Meta:
        model = operacaoOPT
        fields = ('id', 'id_temp','optcode')
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


#DEVO ADICIONAR SERIALIZADORES PARA AS OUTRAS ENTIDADES COM PREFIXO "TEMP" TAMBÉM

class Temp_AgenteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Temp_Agente
        fields=('id','id_user','saldo','celular')

class Temp_ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Temp_Cliente
        fields=('id','id_user','celular')

class Temp_ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Temp_Conta
        fields=('id','id_client','numero','data_abertura','saldo')

class Temp_DepositoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Temp_Deposito
        #nesse caso, o id_agent sera obtido atravez do token de autenticacao do usuario
        fields=('id','id_operacao')

class Temp_LevantamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Temp_Levantamento
        fields=('id','id_agent','id_operacao')

class Temp_TransferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Temp_Transferencia
        fields=('id','id_agent','id_operacao','numero_conta')

