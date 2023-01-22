import regex as re

print("Measure the same thing five times and input the measurements below:")
nbrs = []
for i in range(5):
    nbrs.append(float(re.sub("\,", ".", input(f"{i}:  "))))
print(f"\nYour average is: {sum(nbrs)/5}")
