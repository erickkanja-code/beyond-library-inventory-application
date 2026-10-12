import json
import os
from abc import ABC
from datetime import date, datetime
from utils import BORROW_TRANSACTIONS_FILE, get_choice, get_text, get_int, get_phone
from book import books, save_books

class Borrower:
    """Represent a person who is registered to borrow books.

    Attributes:
        full_name (str): The borrower's full name.
        phone_number (str): The borrower's mobile number.
    """
    def __init__(self, full_name, phone_number):
        self.full_name = full_name
        self.phone_number = phone_number

class BorrowTransaction:
    """Represent one borrowing event in the borrowing history.

    Attributes:
        borrower (str): The full name of the person who borrowed the book.
        title (str): The title of the borrowed book.
        date_borrowed (str): The date the book was borrowed (YYYY-MM-DD).
        date_returned (str | None): The date the book was returned
            (YYYY-MM-DD), or None while it is still borrowed.
    """
    date_returned = None
    def __init__(self, borrower, title, date_borrowed):
        self.borrower = borrower
        self.title = title
        self.date_borrowed = date_borrowed






def save_borrow_transactions():
    """Write the full borrowing history to borrow_transactions.json.

    Each BorrowTransaction is converted to a dictionary with all four
    fields written out explicitly, including date_returned, which is a
    class attribute and would otherwise be missing from the saved data.
    """
    data = {}
    for id, transaction in borrow_transactions.items():
        data[str(id)] = {
            "borrower": transaction.borrower,
            "title": transaction.title,
            "date_borrowed": transaction.date_borrowed,
            "date_returned": transaction.date_returned,
        }
    with open(BORROW_TRANSACTIONS_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_borrow_transactions():
    """Read the borrowing history saved in borrow_transactions.json.

    Returns:
        dict: A dictionary mapping integer ids to BorrowTransaction
        objects. An empty dictionary is returned if the file does not
        exist yet or cannot be read as valid JSON.
    """
    try:
        with open(BORROW_TRANSACTIONS_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    transactions = {}
    for id, details in data.items():
        transaction = BorrowTransaction(
            details["borrower"], details["title"], details["date_borrowed"]
        )
        transaction.date_returned = details["date_returned"]
        transactions[int(id)] = transaction
    return transactions





def borrow_book():
    """Register a borrower if needed and record a book being borrowed.

    Asks whether the user already has a borrower ID, creates a new
    borrower when they do not, then marks the chosen book as borrowed,
    adds a BorrowTransaction to the borrowing history and saves the
    books and the borrowing history to their JSON files.
    """
    # title = input("Enter the title/author:")
    borrower_status = get_choice("Do you have an ID (Enter 1 or 2)?\n 1. Yes 2. No", (1, 2))

    if borrower_status == 1:
        pass
    elif borrower_status == 2:
        full_name = get_text("Enter your full name:")
        phone_number = get_phone("Enter your mobile number:")
        id = len(borrowers)
        new_borrower = Borrower(full_name, phone_number)
        borrowers[id] = new_borrower
        print(f"Account succesfully created. Your borrower id is {id}")
    else:
        print("You entered an incorrect option. Choose either 1 or 2")
        borrow_book()

    borrower_id = get_int("Enter your ID:")
    if borrower_id not in borrowers:
        print("No borrower was found with that ID.")
        return
    borrower_name = borrowers[borrower_id].full_name
    title = get_text("Enter the title of the book you want to borrow:")
    borrow_transaction_id = len(borrow_transactions)
    found = False
    for id in books:
        book = books[id]
        if (title.strip().lower() == book.title.strip().lower()):
            found = True
            if book.status == True:
                print("Book has already been borrowed.")
                return
            book.status = True
            new_borrow_transaction = BorrowTransaction(borrower_name, title, str(date.today()))
            borrow_transactions[borrow_transaction_id] = new_borrow_transaction
            save_books()
            save_borrow_transactions()
            print("Succesfully recorded the transaction.")
    if not found:
        print("No book was found with that title.")

def return_book():
    """Mark a borrowed book as returned and record the return date.

    Finds the book by title, sets it back to not borrowed, stamps today's
    date on the matching borrowing history entry and saves the books and
    the borrowing history to their JSON files.
    """
    title = get_text("Enter the book title:")
    found = False
    for id in books:
        book = books[id]
        if title.strip().lower() == book.title.strip().lower():
            found = True
            if not book.status:
                print("This book was not borrowed")
                return
            book.status = False
            for id in borrow_transactions:
                transaction = borrow_transactions[id]
                if transaction.title.lower() == title.strip().lower():
                    transaction.date_returned = str(date.today())
                    print("Book successfully returned")
            save_books()
            save_borrow_transactions()
    if not found:
        print("No book was found with that title.")
        
borrowers = {}
borrow_transactions = load_borrow_transactions()
