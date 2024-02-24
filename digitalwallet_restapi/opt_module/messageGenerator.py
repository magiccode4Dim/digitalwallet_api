import json
#modulo que Retorna as Mensagens OPT que sao enviadas

def mensagem_de_validacao_de_conta(optcode,cell):
    conteudo = f"Ewallet - Código de Validação de Conta {optcode}."
    return json.dumps({"cell": cell, "message": conteudo})

def mensagem_de_abertura_de_conta(optcode,cell,dataabertura):
    conteudo = f"Ewallet - Registramos uma requisição de abertura de uma conta na data {dataabertura.strftime('%d/%m/%Y %H:%M:%S')}.\n Confirme essa operação com o código {optcode}. Caso desconheça essa operação entre em contacto connosco."
    return json.dumps({"cell": cell, "message": conteudo})

def mensagem_de_confirmacao_de_deposito(optcode,cell,numeroconta,valor,datadeposito,nomecliente):
    conteudo = f"Ewallet - Deposito no valor de {valor} MT na conta {numeroconta} pertencente a {nomecliente}, na data {datadeposito.strftime('%d/%m/%Y %H:%M:%S')}. Confirme a Operação com o código {optcode}."
    return json.dumps({"cell": cell, "message": conteudo})
#mensagens finais
def mensagem_deposito_feito_para_agente(cell,numeroconta,valor,datadeposito,nomecliente,saldoactualagente):
    conteudo = f"Ewallet - Deposito no valor de {valor} MT na conta {numeroconta} pertencente a {nomecliente}, na data {datadeposito.strftime('%d/%m/%Y %H:%M:%S')}. Seu saldo actual é de {saldoactualagente} MT."
    return json.dumps({"cell": cell, "message": conteudo})

def mensagem_deposito_feito_para_cliente(cell,numeroconta,valor,datadeposito,nomeagente, numero, saldoactualconta):
    conteudo = f"Ewallet - O agente {numero} - {nomeagente}, depositou {valor} MT na conta sua conta {numeroconta}, na data {datadeposito.strftime('%d/%m/%Y %H:%M:%S')}. O saldo actual da dessa conta é {saldoactualconta} MT"
    return json.dumps({"cell": cell, "message": conteudo})

def mensagem_de_confirmacao_de_levantamento(cell,nomecliente,nomeagente,codigoagente,valor,numeroconta,datalevantamento,optcode):
    conteudo = f"Ewallet - Caro {nomecliente}, registramos um levantamento no agente {codigoagente} - {nomeagente}, no valor de {valor} MT, na conta {numeroconta}, na data {datalevantamento.strftime('%d/%m/%Y %H:%M:%S')}. Confirme a Operação com o código {optcode}."
    return json.dumps({"cell": cell, "message": conteudo})
#mensagens finais
def mensagem_levantamento_feito_para_agente(cell,numeroconta,valor,datadeposito,nomecliente,saldoactualagente):
    conteudo = f"Ewallet - Levantou {valor} MT na conta {numeroconta}, na data {datadeposito.strftime('%d/%m/%Y %H:%M:%S')}. Seu saldo actual é de {saldoactualagente} MT."
    return json.dumps({"cell": cell, "message": conteudo})
def mensagem_levantamento_feito_para_cliente(cell,numeroconta,valor,datadeposito,nomeagente, numero, saldoactualconta):
    conteudo = f"Ewallet - Levantou {valor} MT na conta sua conta {numeroconta}, no agente  {numero} - {nomeagente}, na data {datadeposito.strftime('%d/%m/%Y %H:%M:%S')}. O saldo actual da dessa conta é {saldoactualconta} MT."
    return json.dumps({"cell": cell, "message": conteudo})

def mensagem_de_confirmacao_de_transferencia(cell,nomecliente,valor,numerocontadestion,donocontadestion,datatransferencia,optcode):
    conteudo = f"Ewallet - Transferencia {valor} MT, para a conta {numerocontadestion} de {donocontadestion}, data {datatransferencia.strftime('%d/%m/%Y %H:%M:%S')}. OTP: {optcode}. "
    return json.dumps({"cell": cell, "message": conteudo})
#mensagens finais
def mensagem_transferencia_feita_cliente_origem(cell,valor,numerocontadestion,donocontadestion,datatransferencia,saldoactual,numerocontaorigem):
    conteudo = f"Ewallet - Transferencia {valor} MT, para a conta {numerocontadestion} de {donocontadestion}, data {datatransferencia.strftime('%d/%m/%Y %H:%M:%S')}. Saldo {numerocontaorigem} é {saldoactual} MT."
    return json.dumps({"cell": cell, "message": conteudo})
def mensagem_transferencia_feita_cliente_destino(cell,valor,numerocontadestion,donocontadestion,datatransferencia,saldoactualconta):
    conteudo = f"Ewallet - Recebeu {valor} MT na conta {numerocontadestion} de {donocontadestion}, na data {datatransferencia.strftime('%d/%m/%Y %H:%M:%S')}.O saldo actual da dessa conta é {saldoactualconta} MT."
    return json.dumps({"cell": cell, "message": conteudo})

