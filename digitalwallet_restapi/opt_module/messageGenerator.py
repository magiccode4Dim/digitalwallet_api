
#modulo que Retorna as Mensagens OPT que sao enviadas

def mensagem_de_validacao_de_conta(optcode,cell):
    conteudo = f"Ewallet - Código de Validação de Conta {optcode}."
    return '{"cell":"'+str(cell)+'","message":"'+str(conteudo)+'"}'


def mensagem_de_validacao_de_transacao(optcode,cell,idtransacao):
    #em desenvolvimento...
    return ""