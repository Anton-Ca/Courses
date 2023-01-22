cur_speed = 90
speed_limit = 80

if cur_speed > speed_limit:
    if (cur_speed - speed_limit) < 5:
        print("Please stop accelerating!")
    else:
        print("Sir you need to break right now!")
else:
    print("Push the pedal to the metal!")
