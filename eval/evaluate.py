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
    fix_summary = []
    try:
        res = df_raw.compare(df_fixed)
    except Exception as e:
        logger.error(f"Error comparing {raw_csv} and {fixed_csv}: {e}")
        return False, None

    # Iterate through the comparison result
    for row in res.index:
        for col in res.columns.get_level_values(0).unique():  # get_level_values(0) gives unique column names
            if not pd.isna(res.at[row, (col, 'self')]):
                raw_value = res.at[row, (col, 'self')]
                # fixed_value may get None if fix failed
                fixed_value = res.at[row, (col, 'other')] if not pd.isna(res.at[row, (col, 'other')]) else ''

                fix_summary.append({
                    'slice': os.path.basename(raw_csv),
                    'row': row,
                    'column': col,
                    'raw_value': raw_value,
                    'fixed_value': fixed_value,
                    'is_fixed': fixed_value != raw_value
                })

    return res.empty, fix_summary
