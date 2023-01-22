n = int(input("\nPick a number between 2 and 100.\nYour pick: "))
prime = True
div = 0

for i in range(2, n):
    if n % i == 0:
        prime = False
        div = i
        break

p = "" if prime else "NOT " 
print(f"\nYour number is {p}a prime number.")
if not prime:
    print(f"{n} is devidable by {div}.\n")
