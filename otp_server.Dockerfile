FROM python:3.10.12

WORKDIR /app

#copiando a aplicacao
COPY otp_server .

RUN pip install -r requirements.txt

