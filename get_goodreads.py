from os import walk
from time import sleep
import re

def get_goodreads(folder="c:/temp/ebooks/"):

    books = cleanup_filenames(folder)
    fetch_rating_from_goodreads(books)
    

def cleanup_filenames(folder):
    books = set()
    for dirpath, dirnames, filenames in walk(folder):
        for filename in filenames:
            name_without_filetype = re.sub(r'\.[^.]*$', '', filename)
            name_without_inside_brackets = re.sub("\(.*?\)|\[.*?\]","",name_without_filetype)
            name_without_digits_book = re.sub(r'\d|book', '', name_without_inside_brackets, flags=re.IGNORECASE)
            name_without_special_characters = re.sub(r'_|\.|-|,| by ', ' ', name_without_digits_book)

            books.add(name_without_special_characters)
   
    return books

def fetch_rating_from_goodreads(books):
    output = "Book, Rating"
    try: 
        for book in books:
            url_prefix = "https://www.goodreads.com/search?utf8=%E2%9C%93&q="
            url_postfix = "&search_type=books"
            search = urllib.parse.quote_plus(book)
            url = url_prefix + search + url_postfix
            page = urllib.request.urlopen(url)
            html_bytes = page.read()
            html = html_bytes.decode("utf-8")

            start_index = html.find("avg rating") - 5
            if start_index == -6:
                rating = "Not found"
            else:    
                rating = html[start_index:start_index + 4]

            output = "{}\n {}, {}".format(output, book, rating)
            print("{} - {}".format(book, rating))
            
            #sleep(3)

    finally:    
        with open('book_ratings.csv', 'w', encoding='utf8') as file:
            file.write(output)


def main():
    get_goodreads()


if __name__ == "__main__":
    main()
