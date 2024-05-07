import pandas as pd
import json

# Data
data = {
    "Airline": ["Air India", "Jet Airways", "IndiGo", "Multiple carriers", "IndiGo", "IndiGo", "Jet Airways"],
    "Date_of_Journey": ["27/06/2019", "18/05/2019", "27/04/2019", "27/05/2019", "15/06/2019", "24/03/2019", "6/06/2019"],
    "Source": [None, "Kolkata", "Banglore", "Delhi", "Banglore", "Banglore", "Delhi"],
    "Destination": ["Cochin", "Banglore", "Delhi", "Cochin", "Delhi", "New Delhi", "Cochin"],
    "Route": ["DEL → GOI → BOM → COK", "CCU → DEL → BLR", "BLR → DEL", "DEL → BOM → COK", "BLR → DEL", "BLR → DEL", "DEL → JAI → BOM → COK"],
    "Dep_Time": ["10:55", "09:35", "06:05", "11:40", "21:15", "04:00", "05:30"],
    "Arrival_Time": ["19:15", "09:45 19 May", "08:50", "21:00", "00:15 16 Jun", "06:50", "04:25 07 Jun"],
    "Duration": ["8h 20m", "24h 10m", "2h 45m", "9h 20m", "3h", "2h 50m", "22h 55m"],
    "Total_Stops": ["2 stops", "1 stop", "non-stop", "1 stop", "non-stop", "non-stop", "2 stops"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Function to impute missing source
def impute_missing_source(route):
    airport_to_city = {
        'DEL': 'Delhi',
        'CCU': 'Kolkata',
        'BLR': 'Banglore',
        'BOM': 'Mumbai',
        'GOI': 'Goa',
        'COK': 'Cochin',
        'JAI': 'Jaipur'
    }
    first_airport_code = route.split(' → ')[0]
    return airport_to_city.get(first_airport_code, "Unknown")

# Impute the missing value in the 'Source' column
missing_index = df[df['Source'].isnull()].index[0]
df.loc[missing_index, 'Source'] = impute_missing_source(df.loc[missing_index, 'Route'])

# Prepare the result in JSON format
result = {
    "row_index": int(missing_index),
    "column_name": "Source",
    "result": df.loc[missing_index, 'Source']
}

# Print the result as JSON with no indent
print(json.dumps(result))

"""exitcode: 0 (execution succeeded)
Code output: {"row_index": 0, "column_name": "Source", "result": "Delhi"}
"""