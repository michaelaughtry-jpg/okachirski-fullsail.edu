import csv

with open("IoT - 23 Import.csv" ) as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)