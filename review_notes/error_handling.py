# https://pythonprogramming.net/handling-exceptions-try-except-python-3/

import csv

with open('example.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    dates = []
    colors = []
    for row in readCSV:
        color = row[3]
        date = row[0]

        dates.append(date)
        colors.append(color)

    print(dates)
    print(colors)

    # now, remember our lists?
    try:
        whatColor = input('What color do you wish to know the date of?:') # with the below exception it was say 'pink' is not in the list
            if whatColor in colors:
                coldex = colors.index(whatColor)
                theDate = dates[coldex]
                print('The date of',whatColor,'is:',theDate)
            else:
                print("Color not found or is not a color")

    except Exception as e: # saves the exception as e #to be more specific you could use NameError. An exception is just a catch all. Try and Except is more of a catch all last resort, should have built in if statments along the way
        print(e) #this exception doesn't seem to want to work now that I added the if else statement

    print("continuing")
