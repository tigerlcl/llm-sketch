import pandas as pd
import json

# Data
data = {
    'Airline': ['IndiGo', 'Jet Airways', 'Jet Airways', 'Jet Airways', 'Vistara', 'IndiGo', 'Air Asia'],
    'Date_of_Journey': ['12/06/2019', '3/06/2019', '15/06/2019', '21/03/2019', '15/03/2019', '3/03/2019', '24/03/2019'],
    'Source': ['Chennai', 'Mumbai', 'Delhi', 'Delhi', None, 'Delhi', 'Kolkata'],
    'Destination': ['Kolkata', 'Hyderabad', 'Cochin', 'Cochin', 'Kolkata', 'Cochin', 'Banglore'],
    'Route': ['MAA → CCU', 'BOM → HYD', 'DEL → LKO → BOM → COK', 'DEL → IXC → BOM → COK', 'MAA → CCU', 'DEL → HYD → COK', 'CCU → DEL → BLR'],
    'Dep_Time': ['22:05', '10:20', '09:25', '06:20', '07:05', '11:55', '07:35'],
    'Arrival_Time': ['00:25 13 Jun', '11:50', '12:35 16 Jun', '04:25 22 Mar', '09:20', '22:20', '19:25'],
    'Duration': ['2h 20m', '1h 30m', '27h 10m', '22h 5m', '2h 15m', '10h 25m', '11h 50m'],
    'Total_Stops': ['non-stop', 'non-stop', '2 stops', '2 stops', 'non-stop', '1 stop', '1 stop']
}

# Create DataFrame
df = pd.DataFrame(data)

# Function to impute missing source
def impute_missing_source(route):
    source_code = route.split(" → ")[0]
    airport_to_city = {
        "MAA": "Chennai",
        "BOM": "Mumbai",
        "DEL": "Delhi",
        "CCU": "Kolkata",
        "HYD": "Hyderabad",
        "IXC": "Chandigarh",
        "LKO": "Lucknow",
        "BLR": "Bangalore"
    }
    return airport_to_city.get(source_code, "Unknown")

# Impute the missing source
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
Code output: {"row_index": 4, "column_name": "Source", "result": "Chennai"}
"""