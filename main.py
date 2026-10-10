class Book:
    def __init__(self, title, author, category, status):
        self.title = title
        self.author = author
        self.category = category
        self.status = status
        





def add_book():
    title = input("What's the book title?")
    author = input("Enter the author's name")
    category = int(input("Select the book category\n1. Physical book\n2. E-Book\n3. Audio Book"))
    status = False
    id = len(books)
    
    new_book = Book(title, author, category, status)
    books[id] = new_book
    print(new_book.category)
    
    
books = {}
while True:
    add_book()
    print(books[0].status)
    
    
    
    
    