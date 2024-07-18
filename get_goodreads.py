from os import walk
from time import sleep
from urllib.request import urlopen
import urllib
import re

def get_goodreads(folder="c:/temp/ebooks/"):
    # get titles of files in folder
    # for each title look up the relevant goodreads page
    # extract the score and the tags (and read by which friend)
    # save the results to a csv

    # print(os.listdir(folder))
    # print(os.path.isfile(folder))
    # print(os.path.isdir(folder))

    books = set()
    for dirpath, dirnames, filenames in walk(folder):
        for filename in filenames:

            name_without_filetype = re.sub(r'\.[^.]*$', '', filename)
            name_without_inside_brackets = re.sub("\(.*?\)|\[.*?\]","",name_without_filetype)
            name_without_digits_by_book = re.sub(r'\d|by|book', '', name_without_inside_brackets, flags=re.IGNORECASE)
            name_without_special_characters = re.sub(r'_|\.|-|,', ' ', name_without_digits_by_book)

            # print(name_without_special_characters)
            books.add(name_without_special_characters)
            # search = urllib.parse.quote_plus(name_without_special_characters)
   
    print(books)
    
    output = "Book, Rating"

    try: 
        for book in books:
            url_prefix = "https://www.goodreads.com/search?utf8=%E2%9C%93&q="
            url_postfix = "&search_type=books"
            print(book)
            search = urllib.parse.quote_plus(book)
            url = url_prefix + search + url_postfix
            page = urlopen(url)
            html_bytes = page.read()
            html = html_bytes.decode("utf-8")

            #todo go to subpage for extra info

            start_index = html.find("avg rating") - 5
            if start_index == -6:
                rating = "Not found"
            else:    
                rating = html[start_index:start_index + 4]

            output = "{}\n {}, {}".format(output, book, rating)
            print("{} - {}".format(book, rating))
            
            sleep(3)

    finally:    

        with open('book_ratings.csv', 'w', encoding='utf8') as file:
            file.write(output)
            



def main():
    get_goodreads()


if __name__ == "__main__":
    main()
