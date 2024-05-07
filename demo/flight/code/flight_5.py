import pandas as pd
import json

# Define the data
data = {
    "Airline": ["IndiGo", "Air India", "IndiGo", "IndiGo", "Vistara", "Jet Airways", "Jet Airways"],
    "Date_of_Journey": ["03/03/2019", "24/03/2019", "15/06/2019", "3/06/2019", "18/05/2019", "6/05/2019", "27/03/2019"],
    "Source": [None, "Kolkata", "Kolkata", "Delhi", "Banglore", "Kolkata", "Delhi"],
    "Destination": ["New Delhi", "Banglore", "Banglore", "Cochin", "Delhi", "Banglore", "Cochin"],
    "Route": ["BLR → DEL", "CCU → DEL → BLR", "CCU → BLR", "DEL → BOM → COK", "BLR → DEL", "CCU → BOM → BLR", "DEL → BOM → COK"],
    "Dep_Time": ["23:30", "07:00", "21:25", "04:55", "19:30", "08:25", "18:15"],
    "Arrival_Time": ["02:20 04 Mar", "08:55 25 Mar", "00:05 16 Jun", "21:00", "22:15", "18:15", "04:25 28 Mar"],
    "Duration": ["2h 50m", "25h 55m", "2h 40m", "16h 5m", "2h 45m", "9h 50m", "10h 10m"],
    "Total_Stops": ["non-stop", "1 stop", "non-stop", "1 stop", "non-stop", "1 stop", "1 stop"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Define the function to impute the missing source
def impute_missing_source(destination, route):
    if destination == "New Delhi" and "DEL" in route:
        return "Banglore"
    return None

# Apply the function to the DataFrame
missing_index = df[df['Source'].isnull()].index[0]
df.at[missing_index, 'Source'] = impute_missing_source(df.loc[missing_index, 'Destination'], df.loc[missing_index, 'Route'])

# Prepare the result in JSON format
result = {
    "row_index": int(missing_index),
    "column_name": "Source",
    "result": df.at[missing_index, 'Source']
}

# Print the result in JSON format with no indent
print(json.dumps(result))

"""exitcode: 0 (execution succeeded)
Code output: {"row_index": 0, "column_name": "Source", "result": "Banglore"}
"""