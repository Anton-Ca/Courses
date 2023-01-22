import re

name = []
civ_number = []
balance = []
interest_rate = []
yearly_balance = []
nbr_of_persons = 2

print(f"Welcome to our bank!")
for person in range(nbr_of_persons):
    name.append(input("Please enter your username: "))
    civ_number.append(input("Please enter your social security number: "))
    balance.append(float(re.sub("\,", '.', input("Please enter how much money you have (SEK): "))))
    interest_rate.append(float(re.sub("\,", '.', input("Please enter the interest rate in percent: "))))
    
    yearly_balance.append(balance[person] * (1 + interest_rate[person]/100))
    
    print(f"\nYour information:")
    print(f"Name : {name[person]}")
    print(f"Civic number : {civ_number[person]}")
    print(f"Balance : {balance[person]} SEK")
    print(f"Interest rate : {interest_rate[person]} %")
    print(f"\nAfter one year you will have {yearly_balance[person]} SEK\n")
    
    yearly_balance[person] += float(re.sub("\,", '.', input("How much money do you want to deposit (SEK)? ")))
    print(f"Your new balance is {yearly_balance[person]} SEK")
    print("\n")
