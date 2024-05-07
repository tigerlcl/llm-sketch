import pandas as pd
import json

# Input data as a dictionary
data = {
    "Airline": ["Air India", "Multiple carriers", "Multiple carriers", "GoAir", "Jet Airways", "Jet Airways", "Jet Airways"],
    "Date_of_Journey": ["12/03/2019", "15/06/2019", "6/03/2019", "1/06/2019", "27/05/2019", "9/05/2019", "1/06/2019"],
    "Source": ["Mumbai", "Delhi", "Delhi", "Delhi", "Mumbai", "Banglore", "Mumbai"],
    "Destination": ["Hyderabad", "Cochin", "Cochin", "Cochin", "Hyderabad", "Delhi", "Hyderabad"],
    "Route": ["BOM → BLR → CCU → BBI → HYD", "DEL → IXU → BOM → COK", "DEL → BOM → COK", "DEL → BOM → COK", "BOM → HYD", "BLR → DEL", "BOM → HYD"],
    "Dep_Time": ["16:50", "17:50", "10:00", "07:00", "02:55", "18:55", "10:20"],
    "Arrival_Time": ["12:25 13 Mar", "01:30 16 Jun", "18:50", "12:55", "04:20", "22:00", "11:50"],
    "Duration": ["19h 35m", "7h 40m", "8h 50m", "5h 55m", "1h 25m", "3h 5m", "1h 30m"],
    "Total_Stops": ["3 stops", "2 stops", "1 stop", None, "non-stop", "non-stop", "non-stop"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Define the function to impute missing stops
def impute_missing_stops(route):
    if route == "DEL → BOM → COK":
        return "1 stop"
    return None  # Default return if no condition matches

# Apply the function to the DataFrame
df['Total_Stops'] = df.apply(lambda row: impute_missing_stops(row['Route']) if pd.isnull(row['Total_Stops']) else row['Total_Stops'], axis=1)

# Find the row with the previously missing value
missing_value_row = df[df['Airline'] == 'GoAir']

# Prepare the result in JSON format
result = {
    "row_index": missing_value_row.index[0],
    "column_name": "Total_Stops",
    "result": missing_value_row['Total_Stops'].values[0]
}

# Print the result in JSON format with no indent
print(json.dumps(result))

"""exitcode: 1 (execution failed)
Code output: Traceback (most recent call last):
  File "/private/var/folders/09/xvpww0g933qc13phh23w26mm0000gn/T/tmpzgp9j8ir/tmp_code_e8325d9d86cad28e0223837b3f93aa4b.py", line 40, in <module>
    print(json.dumps(result))
  File "/Users/tigerli/miniconda3/envs/llm-sketch/lib/python3.10/json/__init__.py", line 231, in dumps
    return _default_encoder.encode(obj)
  File "/Users/tigerli/miniconda3/envs/llm-sketch/lib/python3.10/json/encoder.py", line 199, in encode
    chunks = self.iterencode(o, _one_shot=True)
  File "/Users/tigerli/miniconda3/envs/llm-sketch/lib/python3.10/json/encoder.py", line 257, in iterencode
    return _iterencode(o, 0)
  File "/Users/tigerli/miniconda3/envs/llm-sketch/lib/python3.10/json/encoder.py", line 179, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type int64 is not JSON serializable
"""