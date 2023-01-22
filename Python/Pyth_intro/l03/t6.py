# Compound formula:
# FV = PV * (1 + r)n
#
# FV = Future value
# PV = Present value (Starting value)
# r = The interest as a decimal value
# n = number of years

pv = 20_000
r = 0.05
n = 20

fv = pv * (1 + r) ** n

print(
    f"After {n} years with a rate of {r} and current value of {pv} you will end up with {fv}kr."
)
print(f"Or rounded of, you will end up with {round(fv)}kr.")
