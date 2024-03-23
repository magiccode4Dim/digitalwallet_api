# digitalwallet_api
# METODO 1 - INICIO (RECOMENDADO)
## INSTALAÇÃO NO DOCKER 
***********
REQUISITOS |
************
1. OS - WINDOWS 10/11 , MACOS, UBUNTU >= 20.04  (recomendado)
2. PYTHON >= 3.8 / PYTHON (3.10.12 -  Usado no projecto)
3. DOCKER >= 25.0.4
4. CONECÇÃO COM A INTERNET
***********************************
1. Clone o Projecto
2. A pasta digitalwallet_api
3. Edite o ficheiro docker-compose.yml de acordo com as suas preferencias (opcional)
4. Rode os Serviços usando o comando : sudo docker-compose up -d

 Por padrão o serviço estaŕá disponivel em : http://127.0.0.1:8000

 ### ACESSANDO CENTRAL DE ADMINISTRADOR
 * URL : http://<SEU_IP>:8000/admin/login/?next=/admin/
 * USERNAME : magiccode
 * PASSWORD: @senhaMu1toF0RT3

 ### SERVIDOR WEBSOCKET MY-OTP
 * URL: ws://<SEU_IP>:3001

 ** NOTA: 
 1. O servidor MY-OTP pode ser conectado na aplicação Android utilizando o ip e porta do servidor.
 2. Pode também ser conectado com o script python presente na pasta otp_client (RECOMENDADO)

 ### CONECTANDO O SERVIDOR MY-OTP VIA SCRIPT PYTHON
 1. Na raiz do projecto, Vá até o directorio otp_client
 2. Instale as dependencias : pip install -r requirements.txt
 3. Rode o script : python3 client_onlyreceived.py
 4. AGUARDE AS MENSAGENS OTP VINDOS DO SERVIDOR

 # METODO 2 - INICIO
 ### INSTAÇÃO MANUAL EM AMBIENTE DE DESENVOLVIMENTO (VSCODE)
 ***********
 REQUISITOS |
 ************
 1. OS - WINDOWS 10/11 , MACOS, UBUNTU >= 20.04  (recomendado)
 2. PYTHON >= 3.8 / PYTHON (3.10.12 -  Usado no projecto)
 3. SERVIDOR POSTGRES DISPONIVEL COM UTILIZADOR VALIDO, IP, PORTA, SENHA
 4. EDITOR VSCODE OU OUTRO
 ************
 
 1. Clone o Projecto
 2. Instale as dependencias presentes nos directorios digitalwallet_api/ otp_client/ e /otp_server usando :
    * pip install -r requirements.txt , em cada termianal aberto nos directorios
 4. Substitua as configurações no arquivo digitalwallet_api/.env de acordo com as suas base de dados.
 5. Crie as migrações e as aplique na base de dados, rodando os seguintes comandos descritos  em digitalwallet_api/:
    * python3 manage.py makemigrations utilizador
    * python3 manage.py makemigrations agente
    * python3 manage.py makemigrations cliente
    * python3 manage.py makemigrations conta
    * python3 manage.py makemigrations operacao
    * python3 manage.py makemigrations deposito
    * python3 manage.py makemigrations levantamento
    * python3 manage.py makemigrations transferencia
    * python3 manage.py migrate --database=default contenttypes
    * python3 manage.py migrate --database=default admin
    * python3 manage.py migrate --database=default auth
    * python3 manage.py migrate --database=default authtoken
    * python3 manage.py migrate --database=default sessions
    * python3 manage.py migrate --database=default utilizador
    * python3 manage.py migrate --database=default agente
    * python3 manage.py migrate --database=default cliente
    * python3 manage.py migrate --database=default conta
    * python3 manage.py migrate --database=default operacao
    * python3 manage.py migrate --database=default deposito
    * python3 manage.py migrate --database=default levantamento
    * python3 manage.py migrate --database=default transferencia
    * python3 manage.py migrate --database=otp_dbtemp opt_module
 6. Crie o superuser usando :
    * python3 manage.py createsuperuser
 7. Rode os servidor My-OTP presente no directorio otp_server/ e rode também o client presente em otp_client/ (em terminais diferentes)
 8. Rode a aplicação usando :
    * python manage.py runserver 0.0.0.0:8000

 


 
