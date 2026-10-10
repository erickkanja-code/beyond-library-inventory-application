from abc import ABC
from datetime import date
class Book(ABC):
    def __init__(self, title, author, date_published, category, status):
        self.title = title
        self.author = author
        self.category = category
        self.status = status
        self.date_published = date_published
        
class Borrower:
    def __init__(self, full_name, phone_number):
        self.full_name = full_name
        self.phone_number = phone_number

class BorrowTransaction:
    date_returned = None
    def __init__(self, borrower, title, date_borrowed):
        self.borrower = borrower
        self.title = title
        self.date_borrowed = date_borrowed



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

def search_book():
    search_entry = input("Enter title of book")
    for id in books:
        book = books[id]
        if (search_entry.strip().lower() 
            in book.title.strip().lower() 
            or search_entry.strip().lower() 
            in book.author.strip().lower()):
            print(f"[{id + 1}] {book.title} written by {book.author} and published on {book.date_published} and {"borrowed" if book.status else "not borrowed"}")

def borrow_book():
    # title = input("Enter the title/author:")
    borrower_status = int(input("Do you have an ID (Enter 1 or 2)?\n 1. Yes 2. No"))
    
    if borrower_status == 1:
        pass
    elif borrower_status == 2:
        full_name = input("Enter your full name:")
        phone_number = input("Enter your mobile number:")
        id = len(borrowers)
        new_borrower = Borrower(full_name, phone_number)
        borrowers[id] = new_borrower
        print(f"Account succesfully created. Your borrower id is {id}") 
    else:
        print("You entered an incorrect option. Choose either 1 or 2")
        borrow_book()
        
    borrower_id = int(input("Enter your ID:"))
    borrower_name = borrowers[borrower_id].full_name
    title = input("Enter the title of the book you want to borrow:")
    borrow_transaction_id = len(borrow_transactions)
    for id in books:
        book = books[id]
        if (title.strip().lower() == book.title.strip().lower()):
            if book.status == True:
                print("Book has already been borrowed.")
                return
            book.status = True
            new_borrow_transaction = BorrowTransaction(borrower_name, title, str(date.today()))
            borrow_transactions[borrow_transaction_id] = new_borrow_transaction
            print("Succesfully recorded the transaction.")
            
def return_book():
    title = input("Enter the book title:")
    for id in books:
        book = books[id]
        if title.strip().lower() == book.title.strip().lower():
            if not book.status:
                print("This book was not borrowed")
            book.status = False
            for id in borrow_transactions:
                transaction = borrow_transactions[id]
                if transaction.title == title.strip().lower():
                    transaction.date_returned = str(date.today())
                    print("Book successfully returned")
             
    
    
    
        

            
    
    
    
    
books = {}
borrowers = {}
borrow_transactions = {}
while True:
    add_book()
    search_book()
    borrow_book()
    return_book()
    for id in borrow_transactions:
        print(borrow_transactions[id].title, borrow_transactions[id].date_returned)

    
    
    
    
    