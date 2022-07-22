import BookGenerator
print('Next Favourite Book')
print('Made by Orlando Scalzo')

NewGenerator = BookGenerator.BookGenerator('main_data.csv')

print('Extending file...')
NewGenerator.extend_file()

print('Type keyword:help for help')

while True:
    name = input('Enter Book Name: ')
    if 'keyword:' in name:
        NewGenerator.keyword_router(name.replace('keyword:', ''))
    else:
        name, search = NewGenerator.find_book_name(name)
        if search:
            NewGenerator.get_book(name)
        else: print('Generating recommendations...')

        if name != '':
            suggestions, book_sum, round_n, amount, threshold= NewGenerator.generate_books(name)
            
            print('You might like: ')

            for i in range(int(amount)):
                percentage = round(100 - suggestions[i][1]/book_sum*100, round_n)
                if percentage > threshold:
                    print(f'{suggestions[i][0]} : {percentage}%')
