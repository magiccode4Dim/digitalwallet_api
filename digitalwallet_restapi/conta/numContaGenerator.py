import random

NUM_CONTA_INTERVAL_BEGIN = 1000000000000000000000
NUM_CONTA_INTERVAL_END = 9999999999999999999999

#gera codigos OPT aleatorio 
def generate_unique_numconta(allcontasList):
        # Gera um código OPT único de 6 dígitos
        contasList = list()
        for c in allcontasList:
            contasList.append(c.numero)
        while True:    
            newconta = random.randint(NUM_CONTA_INTERVAL_BEGIN,NUM_CONTA_INTERVAL_END)
            if newconta not in contasList:
                return newconta
