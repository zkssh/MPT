import pandas as pd
import sys
import os

# Check if a file name was provided
if len(sys.argv) < 2:
    print("Please provide a CSV file as an argument.")
    sys.exit(1)

# Get the file name from the command line arguments
input_file_name = sys.argv[1]

# Check if the provided file exists and is a CSV
if not os.path.isfile(input_file_name) or not input_file_name.lower().endswith('.csv'):
    print("The provided file does not exist or is not a CSV file.")
    sys.exit(1)

# Read the CSV file
data = pd.read_csv(input_file_name)

# Convert the DataFrame to JSON
json_data = data.to_json(orient='records')

# Generate the output file name by replacing the .csv extension with .json
output_file_name = os.path.splitext(input_file_name)[0] + '.json'

# Write the JSON data to the output file
with open(output_file_name, 'w') as json_file:
    json_file.write(json_data)

print(f"JSON file created: {output_file_name}")

