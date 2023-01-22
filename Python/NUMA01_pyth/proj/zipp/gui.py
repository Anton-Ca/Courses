from datetime import datetime
import plot as plt
import preprocess as prs
import pandas as pd
from tqdm import tqdm


response = input("Use old data? (y)\n")
if response == "y":
    use_saved_data = True
else:
    use_saved_data = False

if use_saved_data:
    bird_data = pd.read_pickle('bird_data.pkl')
    birdPd_m = pd.read_pickle('birdPd_m.pkl')
    birdDiff_m = pd.read_pickle('birdDiff_m.pkl')
    birdDiff = pd.read_pickle('birdDiff.pkl')

    print("Welcome to Bird")
    print("Print help to get list of commands")

else:
    print("Runs preprocessing")
    bird_data = prs.run_pre_process()
    print("Calculate difference between counts")
    birdDiff = plt.diff(bird_data) #
    birdDiff.to_pickle('bird_data.pkl')
    print("Aggregate to minutes for accumaltive")
    birdPd_m = plt.datePerMinute(bird_data)
    birdPd_m.to_pickle('birdPd_m.pkl')
    print("Aggregate to minutes for difference between counts")
    birdDiff_m = plt.datePerMinute(birdDiff) # aggregate to minutes
    birdDiff_m.to_pickle('birdDiff_m.pkl')
    print("Creates column that says if line is on day or night")
    bird_data = plt.isDayTime(bird_data)
    bird_data.to_pickle("bird_data.pkl")
    print("Creates column that says if line is on day or night for diff")
    birdDiff_m = plt.isDayTime(birdDiff_m)
    birdDiff_m.to_pickle("birdDiff_m.pkl")
    print("Welcome to Bird")
    print("Print help to get list of commands")

def modes():
    print("Enter 'cus' to customize plot")
    print("Enter 'pre' to get precustomized plots")


def help_graph():
    print("Enter 'exit' to close program.")
    print("There are two modes for printing graphs")
    modes()


last_command = " "
while last_command != "exit":
    modes()
    last_command = input()


    if last_command == "help":
        help_graph()

    elif last_command == "cus":
        print("Enter start date: \nExample of valid input: 2015-08-5 9:31")
        print("Must be between 2015-01-25 14:05 and 2016-01-16 17:22")
        strDate = input()

        dateForm = '%Y-%m-%d %H:%M'
        try:
            date = strDate #datetime.timestamp(datetime.strptime(strDate, dateForm))
        except:
            raise ValueError("Invalid format")
        numDays = input("Input number of dates from date to show:\n")
        try:
            numDays = int(numDays)
        except:
          raise ValueError("Invalid input.")



        plot_type = input("enter plot type, normal or night: \n")

        if plot_type == "normal":
            intervals = input("Interval, total per hour(1), total per day(2), total per week(3), total per month(4), total per year(5):\n")
            try:
                intervals = int(intervals)
            except:
                raise ValueError("Invalid input.")

            try:
                plt.normalPlot(birdPd_m, date, numDays, intervals)
            except:
                raise ValueError("Illegal input to ploting function")

        elif plot_type == "night":
            plt.drawNight(birdDiff_m, date, numDays)
        else:
            print("Invalid plot type")

    elif last_command == "pre":
        # plots
        plt.deBugPlot(bird_data)
        plt.deBugPlot(birdDiff)
        plt.drawNight(bird_data, '2015-10-14 08:00', 10)
        plt.drawNight(birdDiff_m, '2015-03-14 08:00', 3)
        plt.normalPlot(birdPd_m, '2015-04-14 08:00', 14, 1)
        plt.bargraphs(birdDiff_m)
