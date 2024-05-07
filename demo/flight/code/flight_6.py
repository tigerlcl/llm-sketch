import pandas as pd
import json

# Input data as a dictionary
data = {
    "Airline": ["Air India", "Jet Airways", "Multiple carriers", "IndiGo", "Multiple carriers", "Jet Airways", "IndiGo"],
    "Date_of_Journey": ["24/05/2019", "15/05/2019", "6/06/2019", "15/05/2019", "3/06/2019", "9/03/2019", "6/06/2019"],
    "Source": ["Kolkata", "Kolkata", "Delhi", "Mumbai", "Delhi", "Delhi", "Kolkata"],
    "Destination": ["Banglore", "Banglore", "Cochin", "Hyderabad", "Cochin", "Cochin", "Banglore"],
    "Route": ["CCU → BOM → COK → BLR", "CCU → DEL → BLR", "DEL → BOM → COK", "BOM → HYD", "DEL → BOM → COK", "DEL → BOM → COK", "CCU → BLR"],
    "Dep_Time": ["09:25", "20:25", "04:55", "02:35", "07:30", "02:15", "15:15"],
    "Arrival_Time": ["13:45 25 May", "14:25 16 May", "19:00", "04:05", "19:15", "19:45", "17:45"],
    "Duration": ["28h 20m", "18h", "14h 5m", "1h 30m", "11h 45m", "17h 30m", "2h 30m"],
    "Total_Stops": ["2 stops", "1 stop", None, "non-stop", "1 stop", "1 stop", "non-stop"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Define the function to impute the missing value based on the route
def impute_total_stops(route):
    if route == "DEL → BOM → COK":
        return "1 stop"
    else:
        return None

# Find the row with the missing 'Total_Stops' and impute it
missing_index = df[df['Total_Stops'].isnull()].index[0]
df.at[missing_index, 'Total_Stops'] = impute_total_stops(df.at[missing_index, 'Route'])

# Prepare the output in JSON format
result = {
    "row_index": int(missing_index),
    "column_name": "Total_Stops",
    "result": df.at[missing_index, 'Total_Stops']
}

# Print the result as JSON with no indent
print(json.dumps(result))

"""exitcode: 0 (execution succeeded)
Code output: {"row_index": 2, "column_name": "Total_Stops", "result": "1 stop"}
"""