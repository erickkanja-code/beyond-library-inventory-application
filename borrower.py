"""Borrower and borrowing-history logic for the Library Inventory Application."""
import json
from datetime import date
from pathlib import Path
from utils import BOOKS_FILE, BORROW_TRANSACTIONS_FILE, get_choice, get_text, get_int, get_phone
from book import books, save_books

BORROWERS_FILE = Path(BOOKS_FILE).with_name("borrowers.json")


class Borrower:
    """Represent a person who is registered to borrow books.

    Attributes:
        full_name (str): The borrower's full name (stored privately).
        phone_number (str): The borrower's mobile number (stored privately).
    """

    def __init__(self, full_name, phone_number):
        self.full_name = full_name
        self.phone_number = phone_number

    @property
    def full_name(self):
        """str: The borrower's full name."""
        return self.__full_name

    @full_name.setter
    def full_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Full name must be a non-empty string.")
        self.__full_name = value.strip()

    @property
    def phone_number(self):
        """str: The borrower's mobile number."""
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = str(value).strip()

    def to_dict(self):
        """Return the borrower as a dictionary that can be saved as JSON."""
        return {"full_name": self.full_name, "phone_number": self.phone_number}

    def __repr__(self):
        return f"Borrower(full_name={self.full_name!r}, phone_number={self.phone_number!r})"

    def __eq__(self, other):
        if not isinstance(other, Borrower):
            return NotImplemented
        return self.phone_number == other.phone_number


class BorrowTransaction:
    """Represent one borrowing event in the borrowing history.

    Attributes:
        borrower (str): The full name of the person who borrowed the book.
        title (str): The title of the borrowed book.
        date_borrowed (str): The date the book was borrowed (YYYY-MM-DD).
        date_returned (str | None): The date the book was returned
            (YYYY-MM-DD), or None while it is still borrowed.
    """

    def __init__(self, borrower, title, date_borrowed, date_returned=None):
        self.borrower = borrower
        self.title = title
        self.date_borrowed = date_borrowed
        self.date_returned = date_returned

    def to_dict(self):
        """Return the transaction as a dictionary that can be saved as JSON."""
        return {
            "borrower": self.borrower,
            "title": self.title,
            "date_borrowed": self.date_borrowed,
            "date_returned": self.date_returned,
        }

    def __repr__(self):
        return (
            f"BorrowTransaction(borrower={self.borrower!r}, title={self.title!r}, "
            f"date_borrowed={self.date_borrowed!r}, date_returned={self.date_returned!r})"
        )


def save_borrowers():
    """Write every registered borrower to borrowers.json."""
    data = {str(id): borrower.to_dict() for id, borrower in borrowers.items()}
    with open(BORROWERS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_borrowers():
    """Read the borrowers saved in borrowers.json.

    Returns:
        dict: A dictionary mapping integer ids to Borrower objects, or an
        empty dictionary if the file is missing or invalid.
    """
    try:
        with open(BORROWERS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return {int(id): Borrower(**details) for id, details in data.items()}


def save_borrow_transactions():
    """Write the full borrowing history to the borrowing history file."""
    data = {str(id): transaction.to_dict() for id, transaction in borrow_transactions.items()}
    with open(BORROW_TRANSACTIONS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_borrow_transactions():
    """Read the borrowing history saved in the borrowing history file.

    Returns:
        dict: A dictionary mapping integer ids to BorrowTransaction
        objects, or an empty dictionary if the file is missing or invalid.
    """
    try:
        with open(BORROW_TRANSACTIONS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return {int(id): BorrowTransaction(**details) for id, details in data.items()}


def find_books_by_title(title):
    """Return a list of books whose title exactly matches (ignoring case)."""
    title = title.strip().lower()
    return [book for book in books.values() if book.title.lower() == title]


def borrow_book():
    """Register a borrower if needed and record a book being borrowed.

    Asks whether the user already has a borrower ID, creates a new
    borrower when they do not, then marks the chosen book as borrowed,
    adds a BorrowTransaction to the borrowing history and saves
    everything to the JSON files.
    """
    borrower_status = get_choice("Do you have an ID (Enter 1 or 2)?\n 1. Yes 2. No", (1, 2))

    if borrower_status == 2:
        full_name = get_text("Enter your full name:")
        phone_number = get_phone("Enter your mobile number:")
        new_borrower = Borrower(full_name, phone_number)
        existing_ids = [id for id, borrower in borrowers.items() if borrower == new_borrower]
        if existing_ids:
            print(f"That phone number is already registered. Your borrower id is {existing_ids[0]}")
        else:
            id = len(borrowers)
            borrowers[id] = new_borrower
            save_borrowers()
            print(f"Account successfully created. Your borrower id is {id}")

    borrower_id = get_int("Enter your ID:")
    if borrower_id not in borrowers:
        print("No borrower was found with that ID.")
        return
    borrower_name = borrowers[borrower_id].full_name

    matches = find_books_by_title(get_text("Enter the title of the book you want to borrow:"))
    if not matches:
        print("No book was found with that title.")
        return
    available = [book for book in matches if not book.status]
    if not available:
        print("Book has already been borrowed.")
        return

    book = available[0]
    book.status = True
    borrow_transactions[len(borrow_transactions)] = BorrowTransaction(
        borrower_name, book.title, str(date.today())
    )
    save_books()
    save_borrow_transactions()
    print("Successfully recorded the transaction.")


def return_book():
    """Mark a borrowed book as returned and record the return date.

    Only the most recent open borrowing record for that title is closed,
    so older history entries keep their original return dates.
    """
    matches = find_books_by_title(get_text("Enter the book title:"))
    if not matches:
        print("No book was found with that title.")
        return
    borrowed = [book for book in matches if book.status]
    if not borrowed:
        print("This book was not borrowed")
        return

    book = borrowed[0]
    book.status = False
    open_transactions = [
        transaction
        for transaction in borrow_transactions.values()
        if transaction.title.strip().lower() == book.title.lower()
        and transaction.date_returned is None
    ]
    if open_transactions:
        open_transactions[-1].date_returned = str(date.today())
    save_books()
    save_borrow_transactions()
    print("Book successfully returned")


borrowers = load_borrowers()
borrow_transactions = load_borrow_transactions()