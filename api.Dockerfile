FROM python:3.10.12

WORKDIR /app

#copiando a aplicacao
COPY digitalwallet_restapi .

RUN pip install -r requirements.txt

