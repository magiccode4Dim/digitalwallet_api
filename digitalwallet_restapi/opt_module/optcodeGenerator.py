import random

#gera codigos OPT aleatorio 
def generate_unique_optcode(otpcodelist):
        # Gera um código OPT único de 6 dígitos
        availablesotps = list()
        for otpcodeOb in otpcodelist:
            availablesotps.append(otpcodeOb.optcode)
        while True:    
            newoptcode = random.randint(100000, 999999)
            if newoptcode not in availablesotps:
                return newoptcode
