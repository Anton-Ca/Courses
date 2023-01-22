print("--- Menu ---")
print("1. Calculate n raised to the power of n")
selected_option = int(input("2. Calculate the sum of the arithmetic series 1, 2, 3, ..., n\n"))

def run_program(option): 
    if option == 1: 
        n = int(input(f"You chose option {option}. Please enter a new integer: \n"))
        print(f"{n**n}")
    elif option == 2:
        n = int(input(f"You chose option {option}. Please enter a new integer: \n"))
        arithmetic_sum = sum([i for i in range(n+1)])
        print(f"{arithmetic_sum}")
    else:
        new_option = int(input("Error! Not a valid option, please type 1 or 2 and then press enter: \n"))
        run_program(new_option)
        
run_program(selected_option)
    
