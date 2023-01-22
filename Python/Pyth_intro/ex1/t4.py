import re
print(f'Welcome to our bank!')
name = input("Please enter your username: ")
civ_number = input('Please enter your social security number: ')
balance = float(re.sub('\,', '.', input("Please enter how much money you have (SEK): ")))
interest_rate = float(re.sub('\,', '.', input("Please enter the interest rate in percent: ")))

yearly_balance = balance * (1 + interest_rate/100)

print(f'\nYour information:')
print(f'Name : {name}')
print(f'Civic number : {civ_number}')
print(f'Balance : {balance} SEK')
print(f'Interest rate : {interest_rate} %')
print(f'\nAfter one year you will have {yearly_balance} SEK')
