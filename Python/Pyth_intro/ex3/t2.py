# Best solution
n = int(input("Please enter a whole number.\n"))
lst = [i for i in range(1, 1+n)]

print(f"The sum of all whole numbers leading up to {n} is: {sum(lst)}")
print(f"The smallest number is: 1")
print(f"The largest number is: {n}")
print(f"The average is: {sum(lst)/n}")



# Loop  
s = 0
for i in range(1, (n + 1)):    
    s += i


# Condition
s = 0
c = 0
while s <= n:
    c += 1
    s += c
