import random

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
