import pandas as pd
import json

# Initialize the DataFrame with the given data
data = {
    "Product line": ["Health and beauty", "Fashion accessories", "Food and beverages", "Fashion accessories", "Sports and travel"],
    "Unit price": [81, 41, 69, 80, 65],
    "Quantity": [7, 10, 8, 7, 2],
    "Tax 5%": [None, 20.5, 27.6, 28.0, 6.5],
    "Total": [595.35, 430.5, 579.6, 588.0, 136.5],
    "Payment": ["Cash", "Cash", "Ewallet", "Credit card", "Credit card"]
}

df = pd.DataFrame(data)

# Define the function to calculate the missing tax
def calculate_tax(unit_price, quantity):
    return unit_price * quantity * 0.05

# Calculate the missing value for "Tax 5%"
missing_tax = calculate_tax(df.loc[0, "Unit price"], df.loc[0, "Quantity"])

# Update the DataFrame with the missing value
df.at[0, "Tax 5%"] = missing_tax

# Prepare the JSON output
result_json = json.dumps({
    "row_index": 0,
    "column_name": "Tax 5%",
    "result": missing_tax
}, indent=None)

# Print the result in JSON format
print(result_json)

"""exitcode: 0 (execution succeeded)
Code output: {"row_index": 0, "column_name": "Tax 5%", "result": 28.35}
"""