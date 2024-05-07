import pandas as pd
import json

# Data
data = {
    "Airline": ["Jet Airways", "IndiGo", "Multiple carriers", "Air India", "Jet Airways", "Jet Airways", "Air Asia"],
    "Date_of_Journey": ["9/06/2019", "1/05/2019", "27/06/2019", "1/04/2019", "01/03/2019", "21/05/2019", "6/05/2019"],
    "Source": ["Kolkata", "Mumbai", "Delhi", "Banglore", "Banglore", "Delhi", "Kolkata"],
    "Destination": ["Banglore", "Hyderabad", "Cochin", "Delhi", "New Delhi", "Cochin", "Banglore"],
    "Route": ["CCU → DEL → BLR", "BOM → HYD", "DEL → BOM → COK", "BLR → DEL", "BLR → BOM → DEL", "DEL → AMD → BOM → COK", "CCU → BLR"],
    "Dep_Time": ["09:35", "09:10", "07:00", "06:10", "16:55", "19:10", "19:55"],
    "Arrival_Time": ["10:55 10 Jun", "10:40", "19:00", "08:55", "09:00 02 Mar", "19:00 22 May", "22:25"],
    "Duration": ["25h 20m", "1h 30m", "12h", "2h 45m", "16h 5m", "23h 50m", "2h 30m"],
    "Total_Stops": ["1 stop", "non-stop", "1 stop", "non-stop", "1 stop", None, "non-stop"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Function to calculate total stops based on the route
def calculate_total_stops(route):
    segments = route.split(" → ")
    if len(segments) > 1:
        return f"{len(segments) - 1} stop" if (len(segments) - 1) == 1 else f"{len(segments) - 1} stops"
    else:
        return "non-stop"

# Find the row with the missing 'Total_Stops' value
missing_index = df[df['Total_Stops'].isnull()].index[0]
missing_route = df.loc[missing_index, 'Route']

# Calculate the missing 'Total_Stops' value
total_stops_calculated = calculate_total_stops(missing_route)

# Update the DataFrame
df.loc[missing_index, 'Total_Stops'] = total_stops_calculated

# Prepare the result in JSON format
result = {
    "row_index": int(missing_index),
    "column_name": "Total_Stops",
    "result": total_stops_calculated
}

# Print the result in JSON format with no indent
print(json.dumps(result))

"""exitcode: 0 (execution succeeded)
Code output: {"row_index": 5, "column_name": "Total_Stops", "result": "3 stops"}
"""