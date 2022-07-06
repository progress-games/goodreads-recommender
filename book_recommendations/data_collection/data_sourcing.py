#data collection
#alot of the stuff when I mess with the webdata will make sense if you have a look
#over the data yourself before it is cleaned.
#3275794 is To Kill a Mockingbird shelf no, what I worked with to do formatting and stuff


def get_shelf(page_no, shelf_items, shelf_ln):
    from bs4 import BeautifulSoup
    from urllib.request import urlopen

    page = urlopen(f'{shelf_ln}?page={page_no}')
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    raw_text = soup.get_text()

    # print(raw_text.replace('\n', '')) use this to see what the raw text looks like and why I'm doing what I'm doing

    #get the book name
    book_name = raw_text[len('Top shelves for '):raw_text.index('Home')]

    # Cut off top and bottom bits from the raw text
    raw_text = list(raw_text[raw_text.index(f'Showing {1+(page_no-1)*100}-{page_no*100}'):raw_text.index("«")].replace(f'Showing {1+(page_no-1)*100}-{page_no*100} of ', '').replace(',', ''))

    #get rid of the number at the start
    for k, v in enumerate(raw_text):
        try:
            int(v)
        except ValueError:
            raw_text = ''.join(raw_text)[k: len(raw_text)]
            break
    
    #clean misc stuff for processing
    cleaned_text = raw_text.replace('\n', '').replace('    ', ':').replace(' people', '').replace(' ', ':')

    #clean misc stuff for viewing
    #view_text = raw_text.replace('\n', '').replace('people    ', 'people\n').replace('    ', ': ')

    word = True
    word_to_add = ''
    number_to_add = ''

    for k, v in enumerate(cleaned_text):
        if not word:
            if v == ':':
                word = True
                shelf_items[word_to_add] = int(number_to_add)
                word_to_add = ''
            else: number_to_add = number_to_add + v
        else:
            if v == ':': 
                word = False
                number_to_add = ''
            else: word_to_add = word_to_add + v

    for k, v in shelf_items.items():
        if v > 100 and page_no < 2:
            shelf_items = shelf_items | get_shelf(page_no+1, {}, shelf_ln)[0]
            break
    
    return shelf_items, book_name.replace('\n', '')[3:len(book_name)]

if __name__ == '__main__':
    print(get_shelf(1, {}, 'https://www.goodreads.com/work/shelves/3532896'))