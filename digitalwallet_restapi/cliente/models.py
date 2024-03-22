from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    celular = models.CharField(max_length=13,default='')
    
#DEVO TRANSFORMAR TODOS OS CADASTROS EM TRANSAÇÕES    
    
#DEVO IMPLEMENTAR A FUNCIONALIDADE DE VERIFICAÇÃO DE PERFILS DE UTILIZADORES, UMA CONTA DE UM UTILIZADOR
#NAO VERIFICADO APRESENTA LIMITES DE TRANSFERENCIA, LEVANTAMNETO E DEPOSITO, PELO QUE, SE A PESSOA QUISER
#FAZER TRANSFERENCIAS APARTIR DE UM DETERMINADO VALOR DEVE VERIFICAR A CONTA COM O SEU BI
#ISSO É UMA MEDIDA PARA A QUESTÃO DE BRANQUEAMENTO DE CAPITAIS


#DEVO IMPLEMENTAR SISTEMA DE LOGS QUE VAI FICAR EM UMA BASE DE DADOS ESPECIFICA PARA ISSO
#CADA OPERACAO/MOVIMENTO QUE CADA UTILIZADOR FIZER, FICARÁ REGISTRADO EM UMA BASE DE DADOS ESPECIAL
# A BASE DE DADOS PODE SER UM MONGO DB


#DEVO IMPLEMENTAR MECANISMOS PARA MEDIR  TAMANHO DOS TEXTOS QUE ENTRAM NA APLICAÇÃO


#DEVO FAZER COM QUE OS ERROS E EXEPÇÕES COM OS MOTIVOS DAS MESMAS, NÃO SEJAM EXPOSTAS PARA O USUARIO EM AMBIENTE
#DE PRODUÇÃO


#DEVO IMPLEMENTAR UM MECANISMO QUE APAGA AS MENSAGENS OTP DEPOIS DE ALGUM TEMPO, DEVE APAGAR OPERACOES SEM DONO TAMBEM
#DEVO LIMITAR O NUMERO DE OPERACOES NAO RESOLVIDAS QUE UM UTILIZADOR PODE CRIAR POR VEZ

#PADRONIZAR OS OUTPUTS, OS VALORES DE RETORNO JSON


#VARIAVEIS DE AMBIENTE DEVEM SER AJUSTAVEIS