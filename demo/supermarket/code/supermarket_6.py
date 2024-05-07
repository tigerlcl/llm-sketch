import pandas as pd
import json

# Initialize the DataFrame with the given data
data = {
    'Product line': ['Health and beauty', 'Home and lifestyle', 'Sports and travel', 'Home and lifestyle', 'Home and lifestyle'],
    'Unit price': [72, 13, 16, 16, 22],
    'Quantity': [7, 2, 10, 2, 9],
    'Tax 5%': [25.2, 1.3, 8.0, 1.6, 9.9],
    'Total': [529.2, 27.3, None, 33.6, 207.9],
    'Payment': ['Cash', 'Credit card', 'Ewallet', 'Ewallet', 'Credit card']
}
df = pd.DataFrame(data)

# Define the function to calculate the missing 'Total' value
def calculate_total(unit_price, quantity, tax):
    return (unit_price * quantity) + tax

# Identify the row with the missing 'Total' value
missing_total_row = df[df['Total'].isnull()]

# Calculate the missing 'Total' value
if not missing_total_row.empty:
    row_index = missing_total_row.index[0]
    unit_price = missing_total_row['Unit price'].iloc[0]
    quantity = missing_total_row['Quantity'].iloc[0]
    tax = missing_total_row['Tax 5%'].iloc[0]
    calculated_total = calculate_total(unit_price, quantity, tax)
    df.at[row_index, 'Total'] = calculated_total  # Fill the missing value in the DataFrame

    # Prepare the result in JSON format
    result_json = json.dumps({
        "row_index": int(row_index),
        "column_name": "Total",
        "result": calculated_total
    }, indent=None)
    print(result_json)

"""exitcode: 0 (execution succeeded)
Code output: {"row_index": 2, "column_name": "Total", "result": 168.0}
"""