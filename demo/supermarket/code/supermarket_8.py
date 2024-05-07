import pandas as pd
import json

# Data initialization
data = {
    "Product line": ["Electronic accessories", "Fashion accessories", "Electronic accessories", "Home and lifestyle", "Home and lifestyle"],
    "Unit price": [82, 21, 97, 45, 33],
    "Quantity": [10, 2, 1, 4, 2],
    "Tax 5%": [41.0, 2.1, 4.85, 9.0, 3.3],
    "Total": [861.0, 44.1, 101.85, None, 69.3],
    "Payment": ["Cash", "Ewallet", "Ewallet", "Credit card", "Credit card"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Function to calculate total
def calculate_total(unit_price, quantity, tax):
    return (unit_price * quantity) + tax

# Find the row with missing 'Total' and calculate it
missing_index = df[df['Total'].isna()].index[0]
unit_price = df.loc[missing_index, 'Unit price']
quantity = df.loc[missing_index, 'Quantity']
tax = df.loc[missing_index, 'Tax 5%']
total = calculate_total(unit_price, quantity, tax)

# Fill the missing value in the DataFrame
df.loc[missing_index, 'Total'] = total

# Prepare the result in JSON format
result = {
    "row_index": int(missing_index),
    "column_name": "Total",
    "result": total
}

# Print the result in JSON format with no indent
print(json.dumps(result))

"""exitcode: 0 (execution succeeded)
Code output: {"row_index": 3, "column_name": "Total", "result": 189.0}
"""