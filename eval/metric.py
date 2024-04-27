import csv


def compare_csv_files(file1, file2):
    try:
        with open(file1, 'r') as csv_file1, open(file2, 'r') as csv_file2:
            reader1 = csv.reader(csv_file1)
            reader2 = csv.reader(csv_file2)

            # Compare the rows of both CSV files
            for row1, row2 in zip(reader1, reader2):
                if row1 != row2:
                    return False
    except FileNotFoundError:
        return False

    return True
