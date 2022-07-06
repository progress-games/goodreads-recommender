class BookGenerator:
    def __init__(self, file_name):
        import csv

        print('Intitating and reading file...')

        self.file_name = 'book_recommendations/' + file_name
        
        #store the file to a list so i dont have to keep reading it
        with open(self.file_name, 'r', encoding = 'utf-8') as f:
            reader = csv.reader(f)
            self.lines = [row for row in reader]
        
        #let the names be a list of the first entry of each row
        self.names = [row[0] for row in self.lines]
        self.names = self.names[1:len(self.names)]

        #let the headers be everything from the first row
        self.headers = [entry for entry in self.lines[0]]
        self.headers = self.headers[1:len(self.headers)]

        self.keywords = {'help': 'Navigates to this menu', 'settings': 'Navigates to settings',
        'quit': 'Exits the program', 'instructions': 'Brief explanation on how to use this program',
        'description': 'Brief description on how this program works'}

        print('Getting data...')
        self.get_data()
        print('Updating settings...')
        self.update_settings()

    def update_settings(self):

        with open('book_recommendations/settings.txt', 'r') as f:
            content = f.readlines()
            self.settings = {}
            self.descriptions = {}
            self.extended_descriptions = {}
            for k, v in enumerate(content):
                setting = ['', '', '', '']
                a = 0
                for char in v:
                    if char != ':': setting[a] = setting[a] + char
                    else: a+=1
                try:
                    setting[1] = int(setting[1])
                except ValueError:
                    if setting[1] == 'True': setting[1] = True
                    else: setting[1] = False
                self.settings[setting[0]] = setting[1]
                self.descriptions[setting[0]] = setting[2].replace('\n', '')
                self.extended_descriptions[setting[0]] = setting[3].replace('\n', '')
        
    def keyword_router(self, area):
        for keyword, _ in self.keywords.items():
            if self.similar(area, keyword, 0.5):
                self.__getattribute__(keyword)()
                
    def help(self):
        print('This is the help menu')

        for keyword, desc in self.keywords.items():
            print(f'keyword:{keyword} : {desc}')
        
        ans = input('Enter a keyword to navigate to that menu, otherwise press enter: ')

        if ans != '':
            self.keyword_router(ans)

    def settings(self):
        print('This is the settings menu')
    
    def quit(self):
        print('This is the quitting menu')
    
    def instructions(self):
        print('This is the instructions menu')

    def description(self):
        from time import sleep
        print('This program was developed solely by Orlando Scalzo for a SAT project during 2022 over approximately 2 months of programming')
        sleep(1)
        print('There are two steps')
        sleep(0.5)
        print('1. Getting data:')
        print('There is a seperate data collector stored in a file within this file which was ran for about 72 hours to collect the ~4000 books')
        sleep(1)
        print('It navigates to lists, gets the link for each book. I encourage you to go to Goodreads.com to try to follow along')
        sleep(0.5)
        print('Then, for each book, it gathers the user-generated shelves and expresses each shelf as a fraction over the total amount of people who shelved the book')
        sleep(1.5)
        print('Then it stores it to a csv called import data, which I then manually appended to main data and ran a short data cleaner script to remove duplicates')
        sleep(1)
        print('2. Generating recommendations')
        print('There is a class (which you\'re interacting with right now) that reads from the book data and generates books from')
        sleep(1)
        print('First it gets your book. Then for each other book, it gets the difference between your book\'s shelf and the other book\'s')
        sleep(1)
        print('It then expresses this as a difference over the maximum possible difference, and subtracts it from 100')
        sleep(1)
        print('There is no machine learning, AI or other cool stuff in this project, just numbers!')
        sleep(1)
        print('Sending you back to the help menu...')
        sleep(1)
        self.help()

    def similar(self, a, b, allowance):
        from difflib import SequenceMatcher
        return SequenceMatcher(None, a, b).ratio() > allowance

    def extend_file(self):
        import csv

        #let the row length be the amount of headers
        row_length = len(self.lines[0])

        #add zeros until each row is the same length
        for k, v in enumerate(self.lines):
            while len(v) < row_length + 1:
                self.lines[k].append(0)

        #rewrite the file (don't need to reread it)
        with open(self.file_name, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.lines)
    
    def get_data(self):
        self.data = {}

        #get the data from the file and chuck it in a dictionary
        for row in self.lines:
            if row[0] != 'name':
                self.data[row[0]] = []
                for entry in row:
                    self.data[row[0]].append(entry)
                self.data[row[0]] = [float(num) for num in self.data[row[0]][1:len(self.data[row[0]])]]

    def get_book(self, book_name):
        from time import sleep

        print('\n--DO NOT INTERACT WITH THE BROWSER--')

        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys

        path = 'C:\Program Files (x86)\chromedriver.exe'

        driver = webdriver.Chrome(path)

        #logs in to disable prompt
        driver.get('https://www.goodreads.com/ap/signin?language=en_US&openid.assoc_handle=amzn_goodreads_web_na&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.goodreads.com%2Fap-handler%2Fsign-in&siteState=39a05fa79cc07d548e50d6cf09db8e17')

        driver.find_element(By.NAME, 'email').send_keys('sca0023@elthamhs.vic.edu.au')
        driver.find_element(By.NAME, 'password').send_keys('123456')
        driver.find_element(By.ID, 'signInSubmit').click()
        
        #searches for the book name
        driver.find_element(By.NAME, 'q').send_keys(book_name + Keys.ENTER)

        element = driver.find_elements(By.CLASS_NAME, 'bookTitle')

        #adds each book to a list
        links = {}
        for e in element:
            links[e.text] = e.get_attribute('href')

        #checks with user which book is the right one
        guesses = []
        a = 0
        while len(guesses) == 0:
            for book, _ in links.items():
                if self.similar(book_name.lower(), book.lower(), a):
                    guesses.append(book)
            a -= 0.1

        print('Did you mean')
        for key, name in enumerate(guesses):
            print(f'{key+1}. {name}')
        
        while True:
            try:
                index = int(input('Type the index of your selection: '))
                book = (guesses[index-1], links[guesses[index-1]])
                break
            except ValueError or IndexError:
                print('Please type a number.')
        
        print(f'Getting {book[0]}\'s data...')

        driver.get(book[1])
        url = driver.current_url
        driver.get(url.replace('/show/', '/shelves/'))
        url = driver.current_url
        driver.quit()

        self.add_book(url)
    
    def add_book(self, book_ln):
        #reuse other functions (lazy)
        from data_collection.data_sourcing import get_shelf
        from data_collection.csv_worker import sort_data
        import csv

        #get the gross raw data
        print('Getting data...')
        name, shelf = get_shelf(1, {}, book_ln.replace('/show/', '/shelves/'))

        print('Rebuilding the csv file (this might take a while!)...')
        
        #adds all new headers
        for k, v in shelf.items():
            for k, v in v.items():
                if k not in self.headers:
                    self.headers.append(k)

        #adds a new line for the new book
        self.lines.append(sort_data(self.headers, name, shelf))

        #rewrite the csv for next time
        with open('book_recommendations/main_data.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)
            writer.writerows(self.lines)
        
        #reinitiates everything to prevent errors
        self.extend_file()
        self.__init__()

        #generates similar books
        self.generate_books(name)
    
    def generate_books(self, book_name):
        book_data = self.data[book_name]

        suggestions_raw = {}

        #gets the difference between each column for each entry
        #if one book has 50 fiction and another 20 the difference is 30 which is added to a running total
        #the lowest total is the highest likely
        for k, _ in self.data.items():
            if k != book_name:
                suggestions_raw[k] = sum([abs(value-self.data[k][key]) for key, value in enumerate(book_data)])
        
        #get the sum of every entry for a book (normally should be 10000)
        book_sum = sum([v for _, v in enumerate(book_data)])

        #sort the suggestions from lowest difference to highest
        suggestions = sorted(suggestions_raw.items(), key=lambda x: x[1])

        return suggestions, book_sum, self.settings['Round to'], self.settings['Suggestion amount'], self.settings['Suggestion threshold']
    
    def find_book_name(self, book_name):
        suggested = []
        a = 0.8

        #find at least one similar book by lowing the allowed threshold
        while len(suggested) == 0:
            for _, v in enumerate(self.names):
                if self.similar(book_name.lower(), v.lower(), a):
                    suggested.append(v)
            a -= 0.1

        print('Note: Adding additional books to the database is not available at this time\nDid you mean?')

        #print out books, the last item will initiate the search on goodreads.com
        for k, v in enumerate(suggested):
            print(f'{k+1}. {v}')
        print(f'{len(suggested)+1}. None of these')

        if self.settings["Enabled 'Search Goodreads.com'"]:
            print(f'{len(suggested)+2}. Search Goodreads.com')

        #allow only numbers
        while True:
            try:
                index = int(input('Type the index of your selection: '))
                break
            except ValueError:
                print('Please type a number.')
        
        #searches for book or just returns the books choice
        if len(suggested)+1 == index:
            print('As this software is a proof of concept, I apologise for not having your book!')
            return '', False
        elif len(suggested)+2 == index:
            print('Searching for book')
            return book_name, True
        else:
            print(f'You selected {suggested[index-1]}')
            return suggested[index-1], False