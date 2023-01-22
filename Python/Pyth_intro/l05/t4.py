import regex as re

nbr = ''

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

while not isfloat(nbr):
    nbr = re.sub("\,", ".", input("Enter a number between 1 and 10.\n"))

while not 1 < float(nbr) < 10:
    nbr = re.sub("\,", ".", input("Enter a number between 1 and 10.\n"))



