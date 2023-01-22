import re

current_balance = 1000
withdrawal = float(re.sub("\,", '.', input(f"Welcome to our bank!\nYou currently have {current_balance}kr in your account. \nHow much would you like to withdraw?\n")))

if current_balance - withdrawal >= 0 and withdrawal % 100 == 0:
    current_balance -= withdrawal
    print(f"Withdrawal successful! \nYour new balance is {current_balance}kr.")
else:
    print("Illegal transactions, aborting!")
