import pandas as pd
import json

# Initialize the DataFrame with the provided data
data = {
    "Product line": ["Sports and travel", "Fashion accessories", "Fashion accessories", "Health and beauty", "Home and lifestyle"],
    "Unit price": [100, 49, 65, 97, 89],
    "Quantity": [9, 9, 1, 2, 9],
    "Tax 5%": [45.0, 22.05, 3.25, 9.7, 40.05],
    "Total": [945.0, 463.05, None, 203.7, 841.05],
    "Payment": ["Credit card", "Cash", "Credit card", "Credit card", "Credit card"]
}

df = pd.DataFrame(data)

# Define the function to calculate the total
def calculate_total(unit_price, quantity, tax):
    return (unit_price * quantity) + tax

# Find the row with the missing 'Total' value
missing_total_row = df[df['Total'].isnull()]

# Calculate the missing 'Total' using the defined function
calculated_total = calculate_total(
    missing_total_row['Unit price'].iloc[0],
    missing_total_row['Quantity'].iloc[0],
    missing_total_row['Tax 5%'].iloc[0]
)

# Fill the missing value in the DataFrame
df.loc[df['Total'].isnull(), 'Total'] = calculated_total

# Prepare the output in the required JSON format
output = {
    "row_index": missing_total_row.index[0],
    "column_name": "Total",
    "result": calculated_total
}

# Print the result in JSON format with no indent
print(json.dumps(output))

"""exitcode: 1 (execution failed)
Code output: Traceback (most recent call last):
  File "/private/var/folders/09/xvpww0g933qc13phh23w26mm0000gn/T/tmplv5bu863/tmp_code_94b21ca37da01d19dcec918674877f50.py", line 41, in <module>
    print(json.dumps(output))
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