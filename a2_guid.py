import csv

# Open the CSV file
with open('duplicates_a2.csv', 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(file)
    
    # Extract the 'a2_guid' column
    a2_guids = [row['a2_guid'] for row in csv_reader]

# Print the extracted values
print(a2_guids)