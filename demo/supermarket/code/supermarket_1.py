import pandas as pd
import json

# Define the data
data = {
    "Product line": ["Fashion accessories", "Electronic accessories", "Health and beauty", "Health and beauty", "Sports and travel"],
    "Unit price": [80, 48, 17, 70, 83],
    "Quantity": [3, 3, 5, 5, 7],
    "Tax 5%": [12.0, 7.2, 4.25, None, 29.05],
    "Total": [252.0, 151.2, 89.25, 367.5, 610.05],
    "Payment": ["Cash", "Credit card", "Credit card", "Ewallet", "Credit card"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Define the function to calculate the missing tax
def calculate_tax(unit_price, quantity):
    return (unit_price * quantity) * 0.05

# Find the row with missing 'Tax 5%' value
missing_index = df[df['Tax 5%'].isnull()].index[0]

# Calculate the missing tax value
missing_tax = calculate_tax(df.loc[missing_index, 'Unit price'], df.loc[missing_index, 'Quantity'])

# Update the DataFrame with the calculated tax
df.at[missing_index, 'Tax 5%'] = missing_tax

# Prepare the result in JSON format
result = {
    "row_index": int(missing_index),
    "column_name": "Tax 5%",
    "result": missing_tax
}

# Print the result in JSON format with no indent
print(json.dumps(result))

"""exitcode: 0 (execution succeeded)
Code output: {"row_index": 3, "column_name": "Tax 5%", "result": 17.5}
"""