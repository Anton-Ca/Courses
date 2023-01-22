name = input("Please enter your username: ")
civ_number = input('Please enter your social security number: ')
balance = float(input("Please enter how much money you have (SEK): "))
interest_rate = float(input("Please enter the interest rate in percent: "))

yearly_balance = balance * (1 + interest_rate/100)

print(f'Name: {name}')
print(f'Social security number: {civ_number}')
print(f'Balance: {balance} SEK')
print(f'Interest rate: {interest_rate} %')
print(f'Balance after one year: {yearly_balance} SEK')
