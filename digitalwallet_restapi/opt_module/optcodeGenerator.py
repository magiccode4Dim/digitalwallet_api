import random
from uuid import uuid4

OPT_CODE_INTERVAL_BEGIN = 100000
OPT_CODE_INTERVAL_END =  999999

#gera codigos OPT aleatorio 
def generate_unique_optcode(otpcodelist):
        # Gera um código OPT único de 6 dígitos
        availablesotps = list()
        for otpcodeOb in otpcodelist:
            availablesotps.append(otpcodeOb.optcode)
        while True:    
            newoptcode = random.randint(OPT_CODE_INTERVAL_BEGIN,OPT_CODE_INTERVAL_END)
            if newoptcode not in availablesotps:
                return newoptcode
            

#gera chaves de agentes para criacao de contas
#pode utilizar uma ou mais listas como base
def generate_random_key(baseLists):
    availablestokens = list()
    for baseList in baseLists:
        for t in baseList:
            availablestokens.append(t.token)
    while True:
        rand_token = uuid4()
        token = str(rand_token)
        if token not in availablestokens:
            return token
        
    
    
    
