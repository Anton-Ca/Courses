import re

lower = float(re.sub("\,", '.', input(f"Please enter lower limit:\n")))
upper = float(re.sub("\,", '.', input(f"Please enter upper limit:\n")))
nbr = float(re.sub(',', '.', input("Please enter a number:\n")))

if lower <= nbr <= upper: 
    print("Your number lies within the limit.")
else:
    print("Your number does not lie within the limit.")
