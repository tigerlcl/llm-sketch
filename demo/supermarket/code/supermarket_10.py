import pandas as pd
import json

# Data initialization
data = {
    "Product line": ["Health and beauty", "Food and beverages", "Home and lifestyle", "Health and beauty", "Fashion accessories"],
    "Unit price": [58, 88, 46, 71, 56],
    "Quantity": [9, 5, 4, 10, 10],
    "Tax 5%": [26.1, 22.0, 9.2, 35.5, 28.0],
    "Total": [548.1, 462.0, 193.2, None, 588.0],
    "Payment": ["Cash", "Cash", "Ewallet", "Cash", "Ewallet"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Define the function to calculate total
def calculate_total(unit_price, quantity, tax):
    return (unit_price * quantity) + tax

# Find the row with the missing 'Total' value
missing_index = df[df['Total'].isnull()].index[0]

# Calculate the missing 'Total' value
missing_total = calculate_total(df.loc[missing_index, 'Unit price'], df.loc[missing_index, 'Quantity'], df.loc[missing_index, 'Tax 5%'])

# Update the DataFrame
df.at[missing_index, 'Total'] = missing_total

# Prepare the result in JSON format
result = {
    "row_index": int(missing_index),
    "column_name": "Total",
    "result": missing_total
}

# Print the result in JSON format with no indent
print(json.dumps(result))

"""exitcode: 0 (execution succeeded)
Code output: {"row_index": 3, "column_name": "Total", "result": 745.5}
"""