import pandas as pd
import json

# Input data in a dictionary format
data = {
    "Product line": ["Home and lifestyle", "Home and lifestyle", "Home and lifestyle", "Health and beauty", "Home and lifestyle"],
    "Unit price": [95, 24, 94, 19, 49],
    "Quantity": [7, 7, 8, 1, 10],
    "Tax 5%": [None, 8.4, 37.6, 0.95, 24.5],
    "Total": [698.25, 176.4, 789.6, 19.95, 514.5],
    "Payment": ["Credit card", "Ewallet", "Ewallet", "Credit card", "Credit card"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Define the function to calculate the missing Tax 5%
def calculate_tax(unit_price, quantity):
    return (unit_price * quantity) * 0.05

# Calculate the missing Tax 5% for the first row
missing_tax = calculate_tax(df.loc[0, "Unit price"], df.loc[0, "Quantity"])
df.at[0, "Tax 5%"] = missing_tax

# Prepare the result in JSON format
result = {
    "row_index": 0,
    "column_name": "Tax 5%",
    "result": missing_tax
}

# Print the result in JSON format with no indent
print(json.dumps(result))

"""exitcode: 0 (execution succeeded)
Code output: {"row_index": 0, "column_name": "Tax 5%", "result": 33.25}
"""