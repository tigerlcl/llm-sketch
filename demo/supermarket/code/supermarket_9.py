import pandas as pd
import json

# Initialize the DataFrame
data = {
    "Product line": ["Food and beverages", "Sports and travel", "Health and beauty", "Electronic accessories", "Health and beauty"],
    "Unit price": [49, 52, 20, 99, 16],
    "Quantity": [7, 10, 5, 1, 3],
    "Tax 5%": [17.15, 26.0, 5.0, None, 2.4],
    "Total": [360.15, 546.0, 105.0, 103.95, 50.4],
    "Payment": ["Credit card", "Cash", "Cash", "Cash", "Cash"]
}

df = pd.DataFrame(data)

# Define the function to calculate the missing tax value
def calculate_tax(unit_price, quantity):
    return (unit_price * quantity) * 0.05

# Find the missing value
missing_index = df[df["Tax 5%"].isnull()].index[0]
missing_tax = calculate_tax(df.loc[missing_index, "Unit price"], df.loc[missing_index, "Quantity"])

# Update the DataFrame with the calculated value
df.at[missing_index, "Tax 5%"] = missing_tax

# Prepare the result in JSON format
result = {
    "row_index": int(missing_index),
    "column_name": "Tax 5%",
    "result": missing_tax
}

# Print the result in JSON format with no indent
print(json.dumps(result))

"""exitcode: 0 (execution succeeded)
Code output: {"row_index": 3, "column_name": "Tax 5%", "result": 4.95}
"""