import os
import json
import argparse
import pandas as pd
import random


def chunk_dirty_slice(args):
    dataset = args.dataset
    columns = [col for col in args.columns.split(',')]
    exp_dir = args.exp_dir
    col_slices = args.col_slices
    num_rows = args.num_rows
    num_missing = args.num_missing

    random.seed(42)  # for reproducibility`

    # Extract base name of the CSV file without extension
    base_name = os.path.splitext(os.path.basename(dataset))[0]

    # Read the CSV into a DataFrame
    df = pd.read_csv(dataset)

    # Ensure directories exist
    slice_dir = os.path.join(exp_dir, 'slice-data')
    os.makedirs(slice_dir, exist_ok=True)

    input_dir = os.path.join(exp_dir, 'input-data')
    os.makedirs(input_dir, exist_ok=True)


    # Loop to create and process slices
    slice_count = 0
    slice_report = list()
    for col in columns:
        for _ in range(col_slices):
            # unifiled file name
            slice_count += 1
            fn = f"{base_name}_{slice_count}.csv"

            # Randomly select row indices without replacement for slicing
            rows_to_select = random.sample(range(len(df)), num_rows)
            slice_df = df.iloc[rows_to_select].copy()

            # Save original slice
            slice_df.to_csv(os.path.join(slice_dir, fn), index=False)

            # reset slice_df index
            slice_df.reset_index(drop=True, inplace=True)
            all_indices = [(row, col) for row in slice_df.index]
            random.shuffle(all_indices)  # for randomness

            # Perform replacements ensuring no cell is processed more than once
            for _ in range(min(num_missing, len(all_indices))):
                row, col = all_indices.pop()  # Pop ensures no repeats
                value = slice_df.at[row, col]
                slice_report.append(
                    {
                        "slice": fn,
                        "row": row,
                        "col": col,
                        "value": value,
                    }
                )

                slice_df.at[row, col] = '?'  # override
                slice_df.to_csv(os.path.join(input_dir, fn), index=False)

    # Save dirty JSON
    input_path = os.path.join(exp_dir, "slice_report.json")
    with open(input_path, 'w', encoding='utf-8') as f:
        json.dump(slice_report, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    # load config
    parser = argparse.ArgumentParser(description="Load Slice Configuration")
    parser.add_argument('--dataset', type=str, help="path to dataset")
    parser.add_argument('--columns', type=str, help='delimited list columns, seperated by comma')
    parser.add_argument('--exp-dir', type=str, help="path to experiment directory")
    parser.add_argument('--col-slices', '-s', type=int, default=5, help="number of slices per column")
    parser.add_argument('--num-rows', '-r', type=int, default=6, help="number of rows per slice")
    parser.add_argument('--num-missing', '-m', type=int, default=1, help="number of missing values per slice")
    args = parser.parse_args()

    chunk_dirty_slice(args)
