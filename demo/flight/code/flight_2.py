import pandas as pd
import json

# Data
data = {
    'Airline': ['Jet Airways', 'Jet Airways', 'Jet Airways', 'IndiGo', 'Jet Airways', 'Air India', 'Jet Airways'],
    'Date_of_Journey': ['24/03/2019', '12/05/2019', '1/06/2019', '18/03/2019', '12/05/2019', '15/06/2019', '9/06/2019'],
    'Source': ['Kolkata', 'Kolkata', 'Delhi', 'Mumbai', 'Kolkata', 'Banglore', 'Delhi'],
    'Destination': ['Banglore', 'Banglore', 'Cochin', 'Hyderabad', 'Banglore', 'Delhi', 'Cochin'],
    'Route': ['CCU → BOM → BLR', 'CCU → BOM → BLR', 'DEL → NAG → BOM → COK', 'BOM → HYD', 'CCU → BOM → BLR', 'BLR → DEL', 'DEL → BOM → COK'],
    'Dep_Time': ['13:55', '08:25', '14:35', '21:20', '16:30', '21:05', '09:00'],
    'Arrival_Time': ['19:40', '09:20 13 May', '12:35 02 Jun', '22:45', '04:40 13 May', '23:55', '19:00'],
    'Duration': ['5h 45m', '24h 55m', '22h', '1h 25m', '12h 10m', '2h 50m', '10h'],
    'Total_Stops': ['1 stop', '1 stop', '2 stops', 'non-stop', None, 'non-stop', '1 stop']
}

# Create DataFrame
df = pd.DataFrame(data)

# Function to impute missing Total_Stops based on Route
def impute_total_stops(route):
    stops_count = route.count('→') - 1
    if stops_count == 0:
        return 'non-stop'
    elif stops_count == 1:
        return '1 stop'
    elif stops_count == 2:
        return '2 stops'
    else:
        return f'{stops_count} stops'

# Find the row with missing Total_Stops
missing_index = df[df['Total_Stops'].isna()].index[0]
missing_route = df.loc[missing_index, 'Route']

# Impute the missing value
imputed_stop = impute_total_stops(missing_route)
df.loc[missing_index, 'Total_Stops'] = imputed_stop

# Prepare the result in JSON format
result = {
    "row_index": int(missing_index),
    "column_name": "Total_Stops",
    "result": imputed_stop
}

# Print the result in JSON format with no indent
print(json.dumps(result))

"""exitcode: 0 (execution succeeded)
Code output: {"row_index": 4, "column_name": "Total_Stops", "result": "1 stop"}
"""