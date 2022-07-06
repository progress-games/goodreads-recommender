#aligning each number by the header name
def sort_data(headers_total, book_name, book_data):

    total = 0
    for _, v in book_data.items(): total = total + v #adds up the total amount of people
    headers = [k for k, _ in book_data.items()] #gets headers
    values = [book_name] #adds name to the start of a new row

    #for each header in headers, if there is a correlating shelf name for that book, add
    #it (where it is the fraction of those people over the total) to the books values, if not, add 0
    for key, header in enumerate(headers_total):
        if header in headers:
            values.append(round(10000*book_data[header]/total, 3))
        elif key != 0: values.append(0)
        
    return values

#basic writing to csv function
def write_to_csv(headers, rows, file_name):
    import csv
    with open(file_name, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

#returning the first row (this returns 'name' however it is sliced upon retrieval)
def get_headers():
    import csv
    with open('data_collection/import_data.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            return row
        return [] #just in case it is empty, preventing errors

#basic reading from csv function. cuts off the top because that's the headers
def get_rows():
    import csv
    with open('data_collection/import_data.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
    return rows[1:len(rows)]