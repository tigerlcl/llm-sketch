import pandas as pd
import json

# Data initialization
data = {
    "Airline": ["SpiceJet", "Vistara", "Multiple carriers", "Multiple carriers", "Jet Airways", "IndiGo", "IndiGo"],
    "Date_of_Journey": ["15/04/2019", "24/03/2019", "27/03/2019", "15/05/2019", "18/05/2019", "24/06/2019", "27/04/2019"],
    "Source": ["Kolkata", "Kolkata", "Delhi", "Delhi", "Kolkata", "Delhi", "Banglore"],
    "Destination": ["Banglore", "Banglore", "Cochin", "Cochin", "Banglore", "Cochin", "Delhi"],
    "Route": ["CCU → BLR", "CCU → DEL → BLR", "DEL → BOM → COK", "DEL → BOM → COK", "CCU → DEL → BLR", "DEL → COK", "BLR → DEL"],
    "Dep_Time": ["22:20", "07:10", "08:25", "11:30", "09:35", "14:20", "21:15"],
    "Arrival_Time": ["00:40 16 Apr", "22:10", "19:15", "19:15", "19:10", "17:35", "00:15 28 Apr"],
    "Duration": ["2h 20m", "15h", "10h 50m", "7h 45m", "9h 35m", "3h 15m", "3h"],
    "Total_Stops": ["non-stop", "1 stop", "1 stop", None, "1 stop", "non-stop", "non-stop"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Function to fix missing total stops based on the route
def fix_missing_total_stops(route):
    segments = route.split(' → ')
    num_stops = len(segments) - 1
    return f'{num_stops} stop' if num_stops == 1 else f'{num_stops} stops'

# Identify the row with missing 'Total_Stops'
missing_index = df[df['Total_Stops'].isnull()].index[0]
missing_route = df.loc[missing_index, 'Route']

# Apply the fixing function
fixed_total_stops = fix_missing_total_stops(missing_route)

# Update the DataFrame
df.loc[missing_index, 'Total_Stops'] = fixed_total_stops

# Prepare the result in JSON format
result = {
    "row_index": int(missing_index),
    "column_name": "Total_Stops",
    "result": fixed_total_stops
}

# Print the result in JSON format with no indent
print(json.dumps(result))

"""exitcode: 0 (execution succeeded)
Code output: {"row_index": 3, "column_name": "Total_Stops", "result": "2 stops"}
"""