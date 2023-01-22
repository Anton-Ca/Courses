import time

# Relationship between speed, distance and time:
# time = distance / speed

distance = input("What is the total amount of metres you would like to travel:\n")
speed = input("What is the estimated average speed? Give answer in metre/second:\n")

t = float(distance) / float(speed)
formatted_time = time.strftime("%H:%M:%S", time.gmtime(t))

print(
    f"It will take approximately {formatted_time} (hh,mm,ss) to arive at your destination."
)
