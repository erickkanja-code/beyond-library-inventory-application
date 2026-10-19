"""Author class and author-based reports for the Library Inventory Application."""


class Author:
    """Represent the author of one or more books.

    Attributes:
        name (str): The author's name (stored privately).
    """

    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        """str: The author's name."""
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Author name must be a non-empty string.")
        self.__name = value.strip()

    def get_books(self, books):
        """Return a list of the books in the library written by this author.

        Args:
            books (dict): A dictionary mapping ids to book objects.
        """
        return [book for book in books.values() if Author(book.author) == self]

    def __repr__(self):
        return f"Author(name={self.name!r})"

    def __eq__(self, other):
        if not isinstance(other, Author):
            return NotImplemented
        return self.name.lower() == other.name.lower()


def get_authors(books):
    """Return a list of unique Author objects, sorted by name.

    Args:
        books (dict): A dictionary mapping ids to book objects.
    """
    unique = {book.author.lower(): Author(book.author) for book in books.values()}
    return sorted(unique.values(), key=lambda author: author.name.lower())


def books_by_author(books):
    """Group the library's books by author.

    Args:
        books (dict): A dictionary mapping ids to book objects.

    Returns:
        dict: Author names mapped to lists of their books.
    """
    return {author.name: author.get_books(books) for author in get_authors(books)}


def show_books_by_author(books):
    """Print a report of every author and the books they wrote."""
    for name, written in books_by_author(books).items():
        print(f"\n{name} ({len(written)} book(s))")
        for book in written:
            print(f"  - {book.describe()}")