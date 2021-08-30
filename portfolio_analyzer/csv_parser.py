import csv

from .models import Row

def get_processed_rows(filepath:str) -> list[Row]:
    i = 0
    rows = []

    with open(filepath, "r") as f:
        reader = csv.reader(f)

        for row in reader:
            i += 1
            if i == 1:
                continue

            rows.append(Row(*row))

    return rows