from random import randint

nbr = randint(0,100)
guess = int(input("Make a guess between 0 and 100.\n"))
guesses = 1

while guess != nbr:
    if guess < nbr:
        guess = int(input(("Your guess was too small, please make a new guess.\n")))
    if guess > nbr:
        guess = int(input(("Your guess was too large, please make a new guess.\n")))

print("Congratulations! Your guess was correct :)")
