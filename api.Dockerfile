FROM python:3.10.12

WORKDIR /app

#copiando a aplicacao
COPY digitalwallet_restapi .

RUN pip install -r requirements.txt
RUN pip install django-rest-swagger
#Copia o script wait-for-it para garantir que os comandos de migracao sejam executados somente quando
#as base de dados estiverem prontas
COPY wait-for-it/wait-for-it.sh wait-for-it.sh
RUN chmod +x wait-for-it.sh