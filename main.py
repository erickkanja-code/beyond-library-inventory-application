from abc import ABC

class Book(ABC):
    def __init__(self, title, author, date_published, category, status):
        self.title = title
        self.author = author
        self.category = category
        self.status = status
        self.date_published = date_published
        





def add_book():
    title = input("What's the book title?")
    author = input("Enter the author's name")
    date_published = input("When was the book published? Use MM-DD-YYY format.")
    category = int(input("Select the book category\n1. Physical book\n2. E-Book\n3. Audio Book"))
    status = False
    id = len(books)
    
    new_book = Book(title, author, date_published, category, status)
    books[id] = new_book
    print(f"{title}'s details saved successfully")
    
def read_all_books():
    for id in books:
        book = books[id]
        print(f"[{id + 1}] {book.title} written by {book.author} and published on {book.date_published}")
    
    
    
    
books = {}
while True:
    add_book()
    read_all_books()

    
    
    
    
    