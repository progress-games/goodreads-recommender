#class that holds shelves, etc

class DataCollector:
    def __init__(self):
        import csv
        
        #the code below was incredibly helpful for picking
        #up where it left off, however wasn't super useful once I started just doing a 
        #whole shelf over night
        '''
        try:
            with open('TEST_DATA.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                self.current_book = len([row for row in reader]) - 1253 # i know this number looks random
                self.current_shelf = round(self.current_book/50-0.5)
                self.current_book = self.current_book - self.current_shelf*50
                if self.current_book == 50: self.current_book = 0
        except:
        '''

        self.current_book = 0
        self.current_shelf = 1

        self.shelf_links = []

    def init_pos(self): return 50 - self.current_book

    def get_shelves(self, ln):
        import link_sourcing
        
        driver = link_sourcing.init()
    
        self.shelf_links = link_sourcing.get_links(driver, self.current_shelf, ln)

        #prevents returning empty lists, recursively calls itself if it's empty
        if len(self.shelf_links) >= 40: driver.quit()
        else: self.get_shelves(ln)

    def get_book_data(self):
        import data_sourcing

        self.book_data = {}

        try:
            #gets the shelf and name of the current book
            shelf, name = data_sourcing.get_shelf(1, {}, self.shelf_links[self.current_book])

            #gets rid of the random bug that sometimes makes the book name to have an 'r ' at the front
            if name[0] + name[1] == 'r ': name = name[2:len(name)]

            #indicate to delete a row without a name
            if name == '': name = 'DELETE THIS ROW'

            #add to a dictionary
            self.book_data[name] = shelf

            #print an update so one can see the data growing
            print(f'{name}: {self.shelf_links[self.current_book]}')
        except IndexError: 
            pass

        '''
        for i in range(20):
            print(self.shelf_links[i+(self.current_book-1)*20], i+(self.current_book-1)*20)
            shelf, name = data_sourcing.get_shelf(1, {}, self.shelf_links[i+(self.current_book-1)*20])
            self.book_data[name] = shelf
            print(f'{name}: {self.shelf_links[i+(self.current_book-1)*20]}, iter = {i}')'''
        
        self.current_book += 1

        if self.current_book >= 50: self.current_book = 0; self.current_shelf += 1        

    def write_to_csv(self):
        import csv_worker

        headers = csv_worker.get_headers()

        #update the headers list with new headers
        for k, v in self.book_data.items():
            for k, v in v.items():
                if k not in headers:
                    headers.append(k)

        rows = csv_worker.get_rows()

        for k, v in self.book_data.items():
            rows.append(csv_worker.sort_data(headers, k, v))

        csv_worker.write_to_csv(headers, rows, 'data_collection/import_data.csv')