import csv

with open('duplicates_4000.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    guids = [row['words_4000_guid'] for row in csv_reader]

print(guids)
