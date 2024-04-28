import os
import pandas as pd


def compare_csv_files(raw_csv, fixed_csv, logger):
    """
    Compare two CSV files at the cell content level after checking for existence and matching shapes.

    Args:
    raw_csv (str): Path to the raw CSV file.
    fixed_csv (str): Path to the fixed or compared CSV file.

    Returns:
    tuple: A tuple containing:
        - bool: True if the files are identical, False otherwise.
        - dict: A list of dictionary summarizing differences, with each difference as a dict entry.
                 If the files are identical, an empty dictionary is returned.
                 If a file is missing or shapes don't match, returns None for the differences part.
    """

    # Check if files exist
    if not (os.path.exists(raw_csv) and os.path.exists(fixed_csv)):
        logger.error("One or both of the files do not exist.")
        return False, None

    # Read both CSV files into DataFrames
    try:
        df_raw = pd.read_csv(raw_csv)
        df_fixed = pd.read_csv(fixed_csv)
    except Exception as e:
        logger.error(f"Error reading CSV files: {e}")
        return False, None

    # Check if both DataFrames have the same shape
    if df_raw.shape != df_fixed.shape:
        logger.error("CSV files do not have the same shape.")
        return False, None

    # Compare DataFrames
    diff_cells = []
    try:
        res = df_raw.compare(df_fixed)
    except Exception as e:
        logger.error(f"Error comparing {raw_csv} and {fixed_csv}: {e}")
        return False, None

    if not res.empty:
        # Iterate through the comparison result
        for row in res.index:
            for col in res.columns.get_level_values(0).unique():  # get_level_values(0) gives unique column names
                if not pd.isna(res.at[row, (col, 'self')]) and not pd.isna(res.at[row, (col, 'other')]):
                    self_value = res.at[row, (col, 'self')]
                    other_value = res.at[row, (col, 'other')]
                    print(f"Row: {row}, Column: {col}, Self Value: {self_value}, Other Value: {other_value}")

                    diff_cells.append({
                        'slice': os.path.basename(raw_csv),
                        'row': row,
                        'column': col,
                        'raw_value': self_value,
                        'fixed_value': other_value
                    })

        return False, diff_cells  # Files are not identical
    else:
        # Files are identical
        return True, {}
