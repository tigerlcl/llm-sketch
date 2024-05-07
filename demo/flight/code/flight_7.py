import pandas as pd
import json

# Define the data
data = {
    "Airline": ["Air India", "Air India", "IndiGo", "Air India", "Jet Airways", "Jet Airways", "IndiGo"],
    "Date_of_Journey": ["21/03/2019", "27/04/2019", "24/03/2019", "15/06/2019", "6/06/2019", "15/06/2019", "21/03/2019"],
    "Source": ["Delhi", "Delhi", "Banglore", "Delhi", None, "Delhi", "Banglore"],
    "Destination": ["Cochin", "Cochin", "New Delhi", "Cochin", "Cochin", "Cochin", "New Delhi"],
    "Route": ["DEL → CCU → BOM → COK", "DEL → COK", "BLR → DEL", "DEL → BLR → COK", "DEL → NAG → BOM → COK", "DEL → JAI → BOM → COK", "BLR → STV → DEL"],
    "Dep_Time": ["06:50", "05:10", "06:00", "06:10", "14:35", "09:40", "11:20"],
    "Arrival_Time": ["19:15 22 Mar", "08:00", "08:45", "23:00", "04:25 07 Jun", "19:00", "15:25"],
    "Duration": ["36h 25m", "2h 50m", "2h 45m", "16h 50m", "13h 50m", "9h 20m", "4h 5m"],
    "Total_Stops": ["2 stops", "non-stop", "non-stop", "1 stop", "2 stops", "2 stops", "1 stop"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Define the function to impute missing source based on the route
def impute_missing_source(route):
    if route:
        return route.split(" → ")[0]
    return None

# Find the row with the missing source
missing_index = df[df['Source'].isnull()].index[0]

# Impute the missing source
df.loc[missing_index, 'Source'] = impute_missing_source(df.loc[missing_index, 'Route'])

# Prepare the result in JSON format
result = {
    "row_index": int(missing_index),
    "column_name": "Source",
    "result": df.loc[missing_index, 'Source']
}

# Print the result in JSON format with no indent
print(json.dumps(result))

"""exitcode: 0 (execution succeeded)
Code output: {"row_index": 4, "column_name": "Source", "result": "DEL"}
"""