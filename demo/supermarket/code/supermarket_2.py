import pandas as pd
import json

# Initialize the DataFrame with the provided data
data = {
    "Product line": ["Electronic accessories", "Electronic accessories", "Health and beauty", "Sports and travel", "Health and beauty"],
    "Unit price": [77, 21, 81, 95, 47],
    "Quantity": [1, 10, 7, 4, 6],
    "Tax 5%": [3.85, 10.5, 28.35, 19.0, 14.1],
    "Total": [None, 220.5, 595.35, 399.0, 296.1],
    "Payment": ["Ewallet", "Cash", "Cash", "Ewallet", "Credit card"]
}

df = pd.DataFrame(data)

# Define the function to calculate the total
def calculate_total(unit_price, quantity, tax):
    return (unit_price * quantity) + tax

# Calculate the missing total for the first row
missing_total = calculate_total(df.loc[0, "Unit price"], df.loc[0, "Quantity"], df.loc[0, "Tax 5%"])

# Update the DataFrame with the calculated total
df.at[0, "Total"] = missing_total

# Prepare the result in JSON format
result_json = json.dumps({
    "row_index": 0,
    "column_name": "Total",
    "result": missing_total
}, indent=None)

# Print the result in JSON format
print(result_json)

"""exitcode: 0 (execution succeeded)
Code output: {"row_index": 0, "column_name": "Total", "result": 80.85}
"""