# Two nested loops

#n = []
#for i in range(1, 11):
#    n = []
#    for j in range(1, 11):
#        n.append(i*j)
#    print(n)


# Two nested loops with exact same output

# for i in range(1, 11):
#     for j in range(1, 11):
#         print(f"{i*j:>4}", end='')
#     print()


# Two nested loops with extra thingies :) 

symb = '*'
vert_dash = "|"
for i in range(1,11):
    if i == 1:
        for a in range(0,11):
            if a == 0:
                print(f"{symb:>3}  |", end='')
                continue
            print(f"{a:>4}", end='')
        print("\n ", f"-"*44)
    for j in range(1,11):
        if j == 1:
            n = 2 - len(str(i))
            print(" "*n, f"{i} {vert_dash:>2}",  end='')
        print(f"{i*j:>4}", end='')
    print()
