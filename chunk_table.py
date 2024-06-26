import os
import json
import argparse
import pandas as pd
from numpy import NaN
import random

from utils.file_io import check_directory


def chunk_dirty_slice(args):
    dataset = args.dataset
    columns = [col for col in args.columns.split(',')]
    num_slices = args.num_slices
    num_rows = args.num_rows

    random.seed(41)  # for reproducibility`

    # Extract base name of the CSV file without extension
    base_name = os.path.splitext(os.path.basename(dataset))[0]

    # Read the CSV into a DataFrame
    df = pd.read_csv(dataset)

    # Loop to create and process slices
    slice_report = dict()
    for i in range(num_slices):
        # unifiled file name
        fn = f"{base_name}_{i + 1}.csv"

        # Randomly select row indices without replacement for slicing
        rows_to_select = random.sample(range(len(df)), num_rows)
        slice_df = df.iloc[rows_to_select].copy()

        # reset slice_df index and save
        slice_df.reset_index(drop=True, inplace=True)
        slice_df.to_csv(os.path.join(slice_dir, fn), index=False)

        # missing value equally distributed by columns
        col = columns[i % len(columns)]
        missing_indices = [(row, col) for row in slice_df.index]
        random.shuffle(missing_indices)  # for randomness

        # start with single missing value for each slice
        row, col = missing_indices.pop()
        value = slice_df.at[row, col]
        slice_report.update({
            fn: {
                "row_index": row,
                "column_name": col,
                "value": value,
            }
        })
        slice_df.at[row, col] = NaN  # override
        slice_df.to_csv(os.path.join(input_dir, fn), index=False)

    # Save slice report as JSON
    report_fp = os.path.join(report_dir, "slice_report.json")
    with open(report_fp, 'w', encoding='utf-8') as f:
        json.dump(slice_report, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    # load config
    parser = argparse.ArgumentParser(description="Load Slice Configuration")
    parser.add_argument('--dataset', type=str, help="path to dataset")
    parser.add_argument('--columns', '-c', type=str, help='tentative dirty columns, seperated by comma')
    parser.add_argument('--exp-dir', type=str, help="path to experiment directory")

    parser.add_argument('--num-slices', '-s', type=int, default=5, help="number of slices from dataset")
    parser.add_argument('--num-rows', '-r', type=int, default=6, help="number of rows per slice")

    args = parser.parse_args()

    # Ensure directories exist
    exp_dir = args.exp_dir
    check_directory(exp_dir)

    slice_dir = os.path.join(exp_dir, 'slice-data')
    check_directory(slice_dir)

    input_dir = os.path.join(exp_dir, 'dirty-data')
    check_directory(input_dir)

    report_dir = os.path.join(exp_dir, 'report')
    check_directory(report_dir)

    chunk_dirty_slice(args)
