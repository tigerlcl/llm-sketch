import pandas as pd

# Data
data = {
    'Airline': ['Jet Airways', 'Multiple carriers', 'Air India', 'Jet Airways', 'Air India', 'Jet Airways'],
    'Date_of_Journey': ['12/03/2019', '1/06/2019', '27/06/2019', '12/05/2019', '18/03/2019', '9/05/2019'],
    'Source': ['Banglore', 'Delhi', 'Delhi', 'Kolkata', 'Chennai', 'Delhi'],
    'Destination': ['New Delhi', 'Cochin', 'Cochin', 'Banglore', 'Kolkata', 'Cochin'],
    'Route': ['BLR → BOM → DEL', 'DEL → BOM → COK', 'DEL → HYD → MAA → COK', 'CCU → BOM → BLR', 'MAA → CCU', 'DEL → BOM → COK'],
    'Dep_Time': ['18:55', '07:30', '13:15', '06:30', '11:40', '08:00'],
    'Arrival_Time': ['10:45 13 Mar', '19:00', '09:25 28 Jun', '18:15', '13:55', '19:00'],
    'Duration': ['15h 50m', '11h 30m', '20h 10m', '11h 45m', '2h 15m', '11h'],
    'Total_Stops': ['1 stop', '?', '2 stops', '1 stop', 'non-stop', '1 stop']
}

# Create DataFrame
df = pd.DataFrame(data)

# Function to estimate stops
def estimate_stops(route):
    segments = route.count('→')
    if segments == 0:
        return 'non-stop'
    elif segments == 1:
        return '1 stop'
    else:
        return f'{segments} stops'

# Apply the function to fix the missing value
df['Total_Stops'] = df.apply(lambda row: estimate_stops(row['Route']) if row['Total_Stops'] == '?' else row['Total_Stops'], axis=1)

# Save DataFrame to CSV
df.to_csv(path_or_buf='Flight_Route_20.csv', index=False)