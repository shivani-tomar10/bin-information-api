import csv

with open("bin_data.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)

    count = sum(1 for row in reader)

print(count)