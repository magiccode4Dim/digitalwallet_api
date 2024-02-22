
#modulo que Retorna as Mensagens OPT que sao enviadas

def mensagem_de_validacao_de_conta(optcode,cell):
    conteudo = f"Ewallet - Código de Validação de Conta {optcode}."
    return '{"cell":"'+str(cell)+'","message":"'+str(conteudo)+'"}'

def mensagem_de_abertura_de_conta(optcode,cell,dataabertura):
    conteudo = f"Ewallet - Registramos uma requisição de abertura de uma conta na data {dataabertura}.\n Confirme essa operação com o código {optcode}. Caso desconheça essa operação entre em contacto connosco."
    return '{"cell":"'+str(cell)+'","message":"'+str(conteudo)+'"}'

def mensagem_de_confirmacao_de_deposito(optcode,cell,numeroconta,valor,datadeposito,nomecliente):
    conteudo = f"Ewallet - Código de Validação do Deposito no valor de {valor} MT na conta {numeroconta} pertencente a {nomecliente}, na data {datadeposito}. Confirme a Operação com o código {optcode}. Caso desconheça essa operação entre em contacto connosco."
    return '{"cell":"'+str(cell)+'","message":"'+str(conteudo)+'"}'
#mensagens finais
def mensagem_deposito_feito_para_agente(cell,numeroconta,valor,datadeposito,nomecliente,saldoactualagente):
    conteudo = f"Ewallet - Confirmado Deposito no valor de {valor} MT na conta {numeroconta} pertencente a {nomecliente}, na data {datadeposito}. Seu saldo actual é de {saldoactualagente} MT."
    return '{"cell":"'+str(cell)+'","message":"'+str(conteudo)+'"}'

def mensagem_deposito_feito_para_cliente(cell,numeroconta,valor,datadeposito,nomeagente, numero, saldoactualconta):
    conteudo = f"Ewallet - O agente {numero} - {nomeagente}, depositou {valor} MT na conta sua conta {numeroconta}, na data {datadeposito}. O saldo actual da dessa conta é {saldoactualconta} MT"
    return '{"cell":"'+str(cell)+'","message":"'+str(conteudo)+'"}'

def mensagem_de_confirmacao_de_levantamento(cell,nomecliente,nomeagente,codigoagente,valor,numeroconta,datalevantamento,optcode):
    conteudo = f"Ewallet - Caro {nomecliente}, registramos um levantamento no agente {codigoagente} - {nomeagente}, no valor de {valor} MT, na conta {numeroconta}, na data {datalevantamento}. Confirme a Operação com o código {optcode}. Caso desconheça essa operação entre em contacto connosco."
    return '{"cell":"'+str(cell)+'","message":"'+str(conteudo)+'"}'
#mensagens finais
def mensagem_levantamento_feito_para_agente(cell,numeroconta,valor,datadeposito,nomecliente,saldoactualagente):
    conteudo = f"Ewallet - O(A) cliente {nomecliente}  levantou {valor} MT na conta {numeroconta}, na data {datadeposito}. Seu saldo actual é de {saldoactualagente} MT."
    return '{"cell":"'+str(cell)+'","message":"'+str(conteudo)+'"}'

def mensagem_levantamento_feito_para_cliente(cell,numeroconta,valor,datadeposito,nomeagente, numero, saldoactualconta):
    conteudo = f"Ewallet - Levantou {valor} MT na conta sua conta {numeroconta}, no agente  {numero} - {nomeagente}, na data {datadeposito}. O saldo actual da dessa conta é {saldoactualconta} MT"
    return '{"cell":"'+str(cell)+'","message":"'+str(conteudo)+'"}'

def mensagem_de_confirmacao_de_transferencia(cell,nomecliente,valor,numerocontadestion,donocontadestion,datatransferencia,optcode):
    conteudo = f"Ewallet - Caro {nomecliente}, registramos uma transferencia para a conta {numerocontadestion} de {donocontadestion}, no valor de {valor} MT, na data {datatransferencia}. Confirme a Operação com o código {optcode}. Caso desconheça essa operação entre em contacto connosco."
    return '{"cell":"'+str(cell)+'","message":"'+str(conteudo)+'"}'
#mensagens finais
def mensagem_transferencia_feita_cliente_origem(cell,valor,numerocontadestion,donocontadestion,datatransferencia,saldoactual,numerocontaorigem):
    conteudo = f"Ewallet - Transferiu {valor} MT para a conta {numerocontadestion} de {donocontadestion}, na data {datatransferencia}. Seu saldo actual da conta {numerocontaorigem} é {saldoactual} MT. "
    return '{"cell":"'+str(cell)+'","message":"'+str(conteudo)+'"}'
def mensagem_transferencia_feita_cliente_destino(cell,valor,numerocontadestion,donocontadestion,datatransferencia,saldoactualconta):
    conteudo = f"Ewallet - Recebeu {valor} MT na conta {numerocontadestion} de {donocontadestion}, na data {datatransferencia}.O saldo actual da dessa conta é {saldoactualconta} MT."
    return '{"cell":"'+str(cell)+'","message":"'+str(conteudo)+'"}'


def mensagem_de_validacao_de_transacao(optcode,cell,idtransacao):
    #em desenvolvimento...
    return ""