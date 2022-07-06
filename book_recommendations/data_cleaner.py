import csv

with open('book_recommendations/main_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)

    rows = [row for row in reader]
    rows_cleaned = []
    to_delete = []
    
    for key, row in enumerate(rows):
        exists = False
        for clean_row in rows_cleaned:
            try:
                if clean_row[0] == row[0]: exists = True
            except IndexError: pass
        try:
            if 'DELETE' in row[0]: exists = True
        except IndexError: pass

        if not exists and len(row) >= 1: rows_cleaned.append(row)

print(len(rows), len(rows_cleaned))

print(len(rows[1]), len(rows[4000]))

with open('book_recommendations/main_data.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows_cleaned)