name = input("Please enter your username: ")
balance = int(input("Please enter how much money you have (SEK): "))
interest_rate = int(input("Please enter the interest rate in percent: "))

yearly_balance = balance * (1 + interest_rate/100)

print(f'Name: {name}')
print(f'Balance: {balance} SEK')
print(f'Interest rate: {interest_rate} %')
print(f'Balance after one year: {yearly_balance} SEK')
