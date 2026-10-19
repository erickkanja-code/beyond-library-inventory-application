"""Book classes and book-related functions for the Library Inventory Application."""
import json
from abc import ABC, abstractmethod
from utils import BOOKS_FILE, get_text, get_date, get_choice


class LibraryResource(ABC):
    """Abstract base class defining the common interface for library items.

    Attributes:
        title (str): The title of the resource (stored privately).
    """

    def __init__(self, title):
        self.title = title

    @property
    def title(self):
        """str: The title of the resource."""
        return self.__title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title must be a non-empty string.")
        self.__title = value.strip()

    @abstractmethod
    def get_type(self):
        """Return a short, readable name for the kind of resource."""

    @abstractmethod
    def describe(self):
        """Return a one-line description of the resource."""

    @abstractmethod
    def to_dict(self):
        """Return the resource as a dictionary that can be saved as JSON."""


class Book(LibraryResource):
    """Represent a physical book in the library.

    Attributes:
        title (str): The title of the book.
        author (str): The name of the book's author.
        date_published (str): The date the book was published.
        status (bool): True if the book is currently borrowed, otherwise False.
    """

    CATEGORY = 1

    def __init__(self, title, author, date_published, status=False):
        super().__init__(title)
        self.author = author
        self.date_published = date_published
        self.status = status

    @property
    def author(self):
        """str: The name of the book's author."""
        return self.__author

    @author.setter
    def author(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Author must be a non-empty string.")
        self.__author = value.strip()

    @property
    def date_published(self):
        """str: The date the book was published."""
        return self.__date_published

    @date_published.setter
    def date_published(self, value):
        self.__date_published = value

    @property
    def status(self):
        """bool: True if the book is currently borrowed."""
        return self.__status

    @status.setter
    def status(self, value):
        if not isinstance(value, bool):
            raise TypeError("Status must be True or False.")
        self.__status = value

    def get_type(self):
        return "Physical book"

    def describe(self):
        state = "borrowed" if self.status else "not borrowed"
        return (
            f"{self.title} written by {self.author} and published on "
            f"{self.date_published} [{self.get_type()}] - {state}"
        )

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "date_published": self.date_published,
            "category": self.CATEGORY,
            "status": self.status,
        }

    def __repr__(self):
        fields = {key: value for key, value in self.to_dict().items() if key != "category"}
        arguments = ", ".join(f"{key}={value!r}" for key, value in fields.items())
        return f"{type(self).__name__}({arguments})"

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return (
            type(self) is type(other)
            and self.title.lower() == other.title.lower()
            and self.author.lower() == other.author.lower()
        )


class EBook(Book):
    """Represent an electronic book. Extends Book with a file format."""

    CATEGORY = 2

    def __init__(self, title, author, date_published, status=False, file_format="Unknown"):
        super().__init__(title, author, date_published, status)
        self.file_format = file_format

    @property
    def file_format(self):
        """str: The file format of the e-book, e.g. PDF or EPUB."""
        return self.__file_format

    @file_format.setter
    def file_format(self, value):
        self.__file_format = value.strip() or "Unknown"

    def get_type(self):
        return "E-Book"

    def describe(self):
        return f"{super().describe()} | Format: {self.file_format}"

    def to_dict(self):
        data = super().to_dict()
        data["file_format"] = self.file_format
        return data


class AudioBook(Book):
    """Represent an audio book. Extends Book with a narrator."""

    CATEGORY = 3

    def __init__(self, title, author, date_published, status=False, narrator="Unknown"):
        super().__init__(title, author, date_published, status)
        self.narrator = narrator

    @property
    def narrator(self):
        """str: The name of the person who narrates the audio book."""
        return self.__narrator

    @narrator.setter
    def narrator(self, value):
        self.__narrator = value.strip() or "Unknown"

    def get_type(self):
        return "Audio Book"

    def describe(self):
        return f"{super().describe()} | Narrator: {self.narrator}"

    def to_dict(self):
        data = super().to_dict()
        data["narrator"] = self.narrator
        return data


BOOK_CLASSES = {1: Book, 2: EBook, 3: AudioBook}


def book_from_dict(details):
    """Create the right kind of book object from a saved dictionary.

    Args:
        details (dict): The saved book data, including its category.

    Returns:
        Book: A Book, EBook or AudioBook object.
    """
    details = dict(details)
    book_class = BOOK_CLASSES.get(details.pop("category", 1), Book)
    return book_class(**details)


def save_books():
    """Write every book record in the books dictionary to the books file.

    Each book is converted to a plain dictionary with to_dict() because
    JSON cannot store custom objects. Keys are converted to strings
    because JSON object keys must be strings.
    """
    data = {str(id): book.to_dict() for id, book in books.items()}
    with open(BOOKS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_books():
    """Read the book records saved in the books file.

    Returns:
        dict: A dictionary mapping integer ids to book objects. An empty
        dictionary is returned if the file does not exist yet or cannot
        be read as valid JSON.
    """
    try:
        with open(BOOKS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return {int(id): book_from_dict(details) for id, details in data.items()}


def add_book():
    """Prompt for a book's details, create the right book object and save it.

    Duplicate books (same type, title and author) are rejected.
    """
    title = get_text("What's the book title?")
    author = get_text("Enter the author's name")
    date_published = get_date("When was the book published? Use MM-DD-YYYY format.")
    category = get_choice(
        "Select the book category\n1. Physical book\n2. E-Book\n3. Audio Book", (1, 2, 3)
    )

    if category == 2:
        file_format = get_text("Enter the file format (e.g. PDF, EPUB):")
        new_book = EBook(title, author, date_published, file_format=file_format)
    elif category == 3:
        narrator = get_text("Enter the narrator's name:")
        new_book = AudioBook(title, author, date_published, narrator=narrator)
    else:
        new_book = Book(title, author, date_published)

    if any(book == new_book for book in books.values()):
        print("This book is already in the library.")
        return

    id = len(books)
    books[id] = new_book
    save_books()
    print(f"{new_book.title}'s details saved successfully")


def print_books(selection, empty_message="No books to show."):
    """Print a numbered list of books, or a message if there are none.

    Args:
        selection (dict): A dictionary mapping ids to book objects.
        empty_message (str): The message shown when selection is empty.
    """
    if not selection:
        print(empty_message)
        return
    for id, book in selection.items():
        print(f"[{id + 1}] {book.describe()}")


def read_all_books():
    """Print every book in the library."""
    print_books(books)


def search_books(query):
    """Find the books whose title or author contains the search text.

    The search ignores case and surrounding spaces.

    Args:
        query (str): The text to look for in titles and author names.

    Returns:
        dict: The matching books, keyed by id.
    """
    query = query.strip().lower()
    return {
        id: book
        for id, book in books.items()
        if query in book.title.lower() or query in book.author.lower()
    }


def get_available_books():
    """Return the books that are not borrowed, keyed by id."""
    return {id: book for id, book in books.items() if not book.status}


def get_borrowed_books():
    """Return the books that are currently borrowed, keyed by id."""
    return {id: book for id, book in books.items() if book.status}


def show_available_books():
    """Print a report of the books that can be borrowed."""
    print_books(get_available_books(), "No books are available right now.")


def filter_borrowed_books():
    """Print a report of the books that are currently borrowed."""
    print_books(get_borrowed_books(), "No books are currently borrowed.")


books = load_books()