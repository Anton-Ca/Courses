# 1)
print("\n1)")

for i in range(1,7):
    print("*" * i)

# 2)
print("\n2)")

for i in range(1,5):
    for j in range(1,6):
        print("*", end='')
    print()


# 3)
print("\n3)")

# Better
#for i in range(10,0, -2):
#    print("*" * i)

# Two loops
cnt = 0
for i in range(1, 6):
    for j in range(1, 11-cnt):
        print("*", end='')
    cnt += 2
    print()

# 4)
print("\n4)")

odd = "* " * 5
even = " *" * 4

for j in range(1, 5):
    if j % 2 != 0:
        print(odd)
    else:
        print(even)

# 5)
print("\n5)")

# And now I'll do the bad two loops solution again...
c = 1
for i in range(1,5):
    for j in range(1, c+1):
        print("*", end='')
    c += c
    print()
    

# In some of the above I decided to do a better solution, in some I only used the desired (bad) solution and in some I provided both.
