import pandas as pd

# Data
data = {
    'Airline': ['Jet Airways', 'Air India', 'Multiple carriers', 'Jet Airways', 'Air India', 'Jet Airways'],
    'Date_of_Journey': ['21/03/2019', '6/03/2019', '12/06/2019', '9/05/2019', '01/03/2019', '15/03/2019'],
    'Source': ['Delhi', 'Mumbai', 'Delhi', 'Kolkata', 'Banglore', 'Banglore'],
    'Destination': ['Cochin', None, 'Cochin', 'Banglore', 'New Delhi', 'New Delhi'],
    'Route': ['DEL → BOM → COK', 'BOM → JDH → DEL → HYD', 'DEL → BOM → COK', 'CCU → BOM → BLR', 'BLR → DEL', 'BLR → BOM → DEL'],
    'Dep_Time': ['15:00', '09:40', '08:45', '20:00', '17:00', '22:50'],
    'Arrival_Time': ['04:25 22 Mar', '23:45', '19:15', '04:40 10 May', '19:45', '07:40 16 Mar'],
    'Duration': ['13h 25m', '14h 5m', '10h 30m', '8h 40m', '2h 45m', '8h 50m'],
    'Total_Stops': ['1 stop', '2 stops', '1 stop', '1 stop', 'non-stop', '1 stop']
}

# Create DataFrame
df = pd.DataFrame(data)

# Function to predict destination
def predict_destination(source, route):
    if 'DEL' in route and 'COK' in route:
        return 'Cochin'
    elif 'CCU' in route and 'BLR' in route:
        return 'Banglore'
    elif 'BLR' in route and 'DEL' in route:
        return 'New Delhi'
    else:
        return 'Unknown'

# Apply the function to fill missing 'Destination'
df['Destination'] = df.apply(lambda row: predict_destination(row['Source'], row['Route']) if pd.isna(row['Destination']) else row['Destination'], axis=1)

# Save DataFrame to CSV
df.to_csv('Flight_Route_1.csv', index=False)