import regex as re
import time

name = 'Not set yet'
phone_number = 'N/A'
balance = 0.0

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def check_err(cancelled, choice):
    global balance 

    print(f"Error! Not a valid amount to {choice}.")
    if choice == "deposit":
        new_choice = re.sub("\,", '.', input(f"Enter a new positive amount to {choice}, or 0 to return to option menu.\n"))
    else: 
        print(f"Your balance is {balance} SEK.")
        new_choice = re.sub("\,", '.', input(f"Enter a new positive amount (maximum {balance} SEK) to {choice}, or 0 to return to option menu.\n"))

    if new_choice == "0":
        bank()
        cancelled = True
    elif choice == "deposit":
        check_deposit(new_choice)
    else:
        check_withdraw(new_choice)
    return cancelled

def check_deposit(deposit):
    global balance
    choice = "deposit"
    cancelled = False

    if not isfloat(deposit):
        cancelled = check_err(cancelled)

    if cancelled == False and isfloat(deposit):
        deposit = float(deposit)
        if 0 <= deposit:
            balance += deposit
            print(f"Your new balance is {balance} SEK.")
        else: 
            _ = check_err(cancelled, choice)

def check_withdraw(withdrawal):
    global balance
    choice = "withdraw"
    cancelled = False

    if not isfloat(withdrawal):
        cancelled = check_err(cancelled, choice)

    if cancelled == False and isfloat(withdrawal):
        withdrawal = float(withdrawal)
        if 0 <= withdrawal <= balance:
            balance -= withdrawal
            print(f"Your new balance is {balance} SEK.")
        else: 
            _ = check_err(cancelled, choice)

def run_program(option): 
    global name
    global phone_number
    global balance 
    
    if option == "1": 
        name = input(f"You chose option {option}. \nPlease enter your name: \n")
        phone_number = input("Please enter your phone number: \n")
        print("",
                f"Welcome to our bank {name}!",
                f"Your phone number is: {phone_number}",
                f"Your current balance is: {balance} SEK"
                , sep="\n")
        time.sleep(2)
        bank()
    elif option == "2":
        print(f"You chose option {option}.")
        deposit = re.sub("\,", '.', input(f"Please enter an amount to deposit: \n"))
        check_deposit(deposit)
        time.sleep(2)
        bank()
    elif option == "3":
        print(f"You chose option {option}.")
        withdrawal = re.sub("\,", '.', input(f"Please enter an amount to withdraw: \n"))
        check_withdraw(withdrawal)
        time.sleep(2)
        bank()
    elif option == "4":
        print("",
                f"Your name is {name}",
                f"Your phone number is: {phone_number}",
                f"Your current balance is: {balance} SEK"
                , sep="\n")
        time.sleep(2)
        bank()
    elif option == "5":
        print("\nThank you for visting the best bank!\n")
    else:
        new_choice = input("Error! Not a valid option, please type 1, 2, 3 or 4 and then press enter to choose from the menu list. Press 0 to show the list again. \n")
        if new_choice == "0":
            time.sleep(2)
            bank()
        else:
            run_program(new_choice)

def bank():

    print("",
            "--- Welcome to the best bank ---",
            "1. Create an account",
            "2. Deposit money",
            "3. Withdraw money",
            "4. Display account",
            "5. To exit the bank\n",
            sep="\n")
    choice = input("Enter choice:\n")   
    run_program(choice)


def main():

    print("Het there user! Press 0 to start the bank application and 1 to exit.")
    bank()

    # OM bank ändras måste jag dubbelkolla check_err

if __name__ == "__main__":
    main()

