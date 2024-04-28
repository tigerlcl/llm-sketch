import os
import json


def read_csv(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_content = csvfile.read()
    return csv_content


def write_txt_file(file_data, fp, mode='w'):
    with open(fp, mode, encoding='utf-8') as f:
        f.write(file_data)


def write_json_file(file_data, fp):
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(file_data, f, ensure_ascii=False, indent=4)


def check_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


