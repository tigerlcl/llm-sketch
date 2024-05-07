import pandas as pd
import json

# Define the data
data = {
    'Airline': ['Jet Airways', 'IndiGo', 'Jet Airways', 'Jet Airways', 'IndiGo', 'Jet Airways', 'Air Asia'],
    'Date_of_Journey': ['9/05/2019', '21/03/2019', '01/03/2019', '21/03/2019', '6/05/2019', '15/05/2019', '24/05/2019'],
    'Source': ['Banglore', None, 'Banglore', 'Delhi', 'Kolkata', 'Kolkata', 'Kolkata'],
    'Destination': ['Delhi', 'Cochin', 'New Delhi', 'Cochin', 'Banglore', 'Banglore', 'Banglore'],
    'Route': ['BLR → DEL', 'DEL → BOM → COK', 'BLR → BOM → DEL', 'DEL → BOM → COK', 'CCU → HYD → BLR', 'CCU → BOM → BLR', 'CCU → IXR → DEL → BLR'],
    'Dep_Time': ['18:55', '10:45', '05:45', '18:15', '15:15', '14:05', '15:10'],
    'Arrival_Time': ['22:00', '21:00', '20:20', '18:50 22 Mar', '20:05', '23:35', '23:30'],
    'Duration': ['3h 5m', '10h 15m', '14h 35m', '24h 35m', '4h 50m', '9h 30m', '8h 20m'],
    'Total_Stops': ['non-stop', '1 stop', '1 stop', '1 stop', '1 stop', '1 stop', '2 stops']
}

# Create DataFrame
df = pd.DataFrame(data)

# Define the function to impute missing source
def impute_missing_source(route):
    first_airport = route.split(" → ")[0]
    airport_to_city = {
        "BLR": "Banglore",
        "DEL": "Delhi",
        "CCU": "Kolkata",
        "BOM": "Mumbai"
    }
    return airport_to_city.get(first_airport, "Unknown")

# Impute the missing value
missing_index = df[df['Source'].isnull()].index[0]
missing_route = df.loc[missing_index, 'Route']
imputed_source = impute_missing_source(missing_route)
df.loc[missing_index, 'Source'] = imputed_source

# Prepare the result in JSON format
result = {
    "row_index": int(missing_index),
    "column_name": "Source",
    "result": imputed_source
}

# Print the result in JSON format with no indent
print(json.dumps(result))

"""exitcode: 0 (execution succeeded)
Code output: {"row_index": 1, "column_name": "Source", "result": "Delhi"}
"""