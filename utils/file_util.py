import os
import json


def read_csv(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_content = csvfile.read()
    return csv_content


def write_file_data(file_data, fp, ext):
    fp = fp + '.' + ext

    # check if dir exists
    os.makedirs(os.path.dirname(fp), exist_ok=True)

    if ext == 'txt':
        with open(fp, 'w') as f:
            f.write(file_data)
    if ext == 'json':
        with open(fp, 'w') as f:
            json.dump(file_data, f, indent=4)

