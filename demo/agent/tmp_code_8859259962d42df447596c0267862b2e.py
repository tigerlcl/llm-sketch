import pandas as pd

# Data
data = {
    'Airline': ['Jet Airways', 'SpiceJet', 'Jet Airways', 'Multiple carriers', 'SpiceJet', 'Jet Airways'],
    'Date_of_Journey': ['9/06/2019', '12/03/2019', '18/05/2019', '6/03/2019', '27/03/2019', '15/03/2019'],
    'Source': ['Delhi', 'Chennai', 'Kolkata', 'Delhi', 'Kolkata', 'Mumbai'],
    'Destination': ['Cochin', 'Kolkata', 'Banglore', 'Cochin', 'Banglore', 'Hyderabad'],
    'Route': ['DEL → JAI → BOM → COK', 'MAA → CCU', 'CCU → BOM → BLR', 'DEL → BOM → COK', 'CCU → BLR', 'BOM → HYD'],
    'Dep_Time': ['05:30', '09:30', '16:30', '12:50', '22:20', '02:55'],
    'Arrival_Time': ['04:25 10 Jun', '12:05', '16:20 19 May', '01:35 07 Mar', '00:40 28 Mar', '04:25'],
    'Duration': ['22h 55m', '2h 35m', '23h 50m', '12h 45m', '2h 20m', '1h 30m'],
    'Total_Stops': ['2 stops', '?', '1 stop', '1 stop', 'non-stop', 'non-stop']
}

# Create DataFrame
df = pd.DataFrame(data)

# Function to determine stops based on the route
def determine_stops(route):
    segments = route.split(' → ')
    num_stops = len(segments) - 1
    if num_stops == 0:
        return 'non-stop'
    elif num_stops == 1:
        return '1 stop'
    else:
        return f'{num_stops} stops'

# Apply the function to fix the missing value in 'Total_Stops'
df['Total_Stops'] = df.apply(lambda row: determine_stops(row['Route']) if row['Total_Stops'] == '?' else row['Total_Stops'], axis=1)

# Save the DataFrame to a CSV file
df.to_csv('Flight_Route_8.csv', index=False)