from data_collector import DataCollector
'''
NewCollector = DataCollector()

for i in range(24):
    NewCollector.get_shelves('https://www.goodreads.com/shelf/show/australia')
    print('https://www.goodreads.com/shelf/show/australia')
    for i in range(50):
        while True:
            try:
                NewCollector.get_book_data()
                break
            except:
                pass
        NewCollector.write_to_csv()
'''
NewCollector = DataCollector()

for i in range(24):
    NewCollector.get_shelves('https://www.goodreads.com/shelf/show/modern')
    print('https://www.goodreads.com/shelf/show/modern')
    for i in range(50):
        while True:
            try:
                NewCollector.get_book_data()
                break
            except:
                pass
        NewCollector.write_to_csv()

NewCollector = DataCollector()

for i in range(24):
    NewCollector.get_shelves('https://www.goodreads.com/shelf/show/translated')
    print('https://www.goodreads.com/shelf/show/translated ')
    for i in range(50):
        while True:
            try:
                NewCollector.get_book_data()
                break
            except:
                pass
        NewCollector.write_to_csv()