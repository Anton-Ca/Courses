# Two nested loops with exact same output

digits = [i for i in range(1,11)]
width = 4
formatted_digits = ''.join(f'{x:>{width}}' for x in digits)
print(f' * |{formatted_digits:>{width}}')
print('-' * ((len(digits)+1) * width))
for i in range(1, 11):
    print(f"{i:>2}",'|', end='')
    for j in range(1, 11):
        print(f"{i*j:>{width}}", end='') # formatterar så att varje digit tar upp minst 4 chars
    print()
