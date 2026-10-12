import json
import os
from abc import ABC
from datetime import date, datetime
from utils import BOOKS_FILE, get_text, get_date, get_choice

class Book(ABC):
    """Represent a single book in the library.

    Attributes:
        title (str): The title of the book.
        author (str): The name of the book's author.
        date_published (str): The date the book was published.
        category (int): The book category (1 = Physical, 2 = E-Book, 3 = Audio Book).
        status (bool): True if the book is currently borrowed, otherwise False.
    """
    def __init__(self, title, author, date_published, category, status):
        self.title = title
        self.author = author
        self.category = category
        self.status = status
        self.date_published = date_published

def save_books():
    """Write every book record in the books dictionary to books.json.

    Each Book object is converted to a plain dictionary because JSON
    cannot store custom objects. Dictionary keys are converted to strings
    because JSON object keys must be strings.
    """
    data = {str(id): vars(book) for id, book in books.items()}
    with open(BOOKS_FILE, "w") as file:
        json.dump(data, file, indent=4)

def load_books():
    """Read the book records saved in books.json.

    Returns:
        dict: A dictionary mapping integer ids to Book objects. An empty
        dictionary is returned if the file does not exist yet or cannot
        be read as valid JSON.
    """
    try:
        with open(BOOKS_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return {int(id): Book(**details) for id, details in data.items()}

def add_book():
    """Prompt for a book's details, create a Book and save it.

    The new book is stored in the books dictionary as not borrowed and
    the updated records are written to books.json.
    """
    title = get_text("What's the book title?")
    author = get_text("Enter the author's name")
    date_published = get_date("When was the book published? Use MM-DD-YYYY format.")
    category = get_choice("Select the book category\n1. Physical book\n2. E-Book\n3. Audio Book", (1, 2, 3))
    status = False
    id = len(books)

    new_book = Book(title, author, date_published, category, status)
    books[id] = new_book
    save_books()
    print(f"{title}'s details saved successfully")

def read_all_books():
    """Print every book in the library with its author and publish date."""
    for id in books:
        book = books[id]
        print(f"[{id + 1}] {book.title} written by {book.author} and published on {book.date_published}")

def search_book(title):
    """Print the books whose title or author contains the search text.

    The search ignores case and surrounding spaces, and each match is
    shown with whether it is currently borrowed.

    Args:
        title (str): The text to look for in book titles and author names.
    """
    # search_entry = input("Enter title of book")
    for id in books:
        book = books[id]
        if (title.strip().lower()
            in book.title.strip().lower()
            or title.strip().lower()
            in book.author.strip().lower()):
            print(f"[{id + 1}] {book.title} written by {book.author} and published on {book.date_published} and {"borrowed" if book.status else "not borrowed"}")

def filter_borrowed_books():
    """Print only the books that are currently borrowed."""
    for id in books:
        book = books[id]
        if book.status == True:
            search_book(book.title)

books = load_books()
