
#modulo que Retorna as Mensagens OPT que sao enviadas

def mensagem_de_validacao_de_conta(optcode,cell):
    conteudo = f"Ewallet - Código de Validação de Conta {optcode}."
    return '{"cell":"'+str(cell)+'","message":"'+str(conteudo)+'"}'

def mensagem_de_abertura_de_conta(optcode,cell,dataabertura):
    conteudo = f"Ewallet - Registramos uma requisição de abertura de uma conta na data {dataabertura}.\n Confirme essa operação com o código {optcode}. Caso desconheça essa operação entre em contacto connosco."
    return '{"cell":"'+str(cell)+'","message":"'+str(conteudo)+'"}'


def mensagem_de_validacao_de_transacao(optcode,cell,idtransacao):
    #em desenvolvimento...
    return ""