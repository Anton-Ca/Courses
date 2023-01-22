current_temperature = 64

if 0 <= current_temperature <= 50:
    print("No or moderate load on the machine")
elif 50 < current_temperature < 80:
    print("Machine is running under heavy load")
elif 80 < current_temperature:
    print("Machine is under extreme load, take action!")
else:
    print("Error, wrong format on given temperature!")
