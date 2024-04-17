import json


def read_csv(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_content = csvfile.read()
    return csv_content


def write_json_data(file_data, fp):
    with open(fp, 'w') as f:
        json.dump(file_data, f, indent=4)
