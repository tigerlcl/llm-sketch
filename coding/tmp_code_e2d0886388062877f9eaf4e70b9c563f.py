import pandas as pd

# Data
data = {
    "Airline": ["Jet Airways", "IndiGo", "IndiGo", "IndiGo", "Jet Airways", "IndiGo", "Air India", "Air India", "Multiple carriers"],
    "Date_of_Journey": ["6/06/2019", "24/06/2019", "21/03/2019", "15/03/2019", "01/03/2019", "3/05/2019", "21/03/2019", "12/03/2019", "12/06/2019"],
    "Source": ["Delhi", "Mumbai", "Delhi", "Banglore", "Banglore", "Banglore", "Mumbai", "Banglore", "Delhi"],
    "Destination": ["Cochin", "Hyderabad", "Cochin", "New Delhi", "New Delhi", "Delhi", "Hyderabad", "New Delhi", "Cochin"],
    "Route": ["DEL → BOM → COK", "BOM → HYD", "DEL → HYD → MAA → COK", "BLR → HYD → DEL", "BLR → BOM → DEL", None, "BOM → HYD", "BLR → BOM → DEL", "DEL → BOM → COK"],
    "Dep_Time": ["18:15", "12:00", "07:35", "16:15", "22:50", "07:10", "21:05", "08:50", "18:15"],
    "Arrival_Time": ["19:00 07 Jun", "13:30", "21:20", "20:35", "21:20 02 Mar", "10:05", "22:25", "23:15", "01:30 13 Jun"],
    "Duration": ["24h 45m", "1h 30m", "13h 45m", "4h 20m", "22h 30m", "2h 55m", "1h 20m", "14h 25m", "7h 15m"],
    "Total_Stops": ["1 stop", "non-stop", "2 stops", "1 stop", "1 stop", "non-stop", "non-stop", "1 stop", "1 stop"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Function to infer missing 'Route'
def infer_route(source, destination):
    if source == "Delhi" and destination == "Cochin":
        return "DEL → BOM → COK"
    elif source == "Mumbai" and destination == "Hyderabad":
        return "BOM → HYD"
    elif source == "Banglore" and destination == "New Delhi":
        return "BLR → BOM → DEL"
    elif source == "Banglore" and destination == "Delhi":
        return "BLR → DEL"
    else:
        return None

# Apply function to fill missing 'Route'
df['Route'] = df.apply(lambda x: infer_route(x['Source'], x['Destination']) if pd.isna(x['Route']) else x['Route'], axis=1)

# Save DataFrame to CSV
df.to_csv('test_003.csv', index=False)