"""Entry point for the Library Inventory Application (command-line menu)."""
from utils import get_choice, get_text
from book import (
    add_book,
    books,
    read_all_books,
    search_books,
    print_books,
    filter_borrowed_books,
    show_available_books,
)
from borrower import borrow_book, return_book
from author import show_books_by_author


def menu():
    """Show the main menu repeatedly and run the function the user picks.

    Every choice is validated. Options that need existing books are
    blocked with a message while the library is empty. The loop ends
    when the user chooses to quit.
    """
    while True:
        choice = get_choice(
            "\n=================================\n"
            "          LIBRARY MENU\n"
            "=================================\n"
            "1. Add a book\n"
            "2. View all books\n"
            "3. Search for a book\n"
            "4. Borrow a book\n"
            "5. Return a book\n"
            "6. View borrowed books\n"
            "7. View available books\n"
            "8. View books by author\n"
            "9. Quit\n"
            "=================================\n"
            "Enter your choice (1-9): ",
            range(1, 10),
        )
        if choice == 1:
            add_book()
        elif choice == 9:
            print("Goodbye!")
            break
        elif not books:
            print("There are no books in the library yet. Add a book first.")
        elif choice == 2:
            read_all_books()
        elif choice == 3:
            query = get_text("Enter a title or author to search for: ")
            print_books(search_books(query), "No books matched your search.")
        elif choice == 4:
            borrow_book()
        elif choice == 5:
            return_book()
        elif choice == 6:
            filter_borrowed_books()
        elif choice == 7:
            show_available_books()
        elif choice == 8:
            show_books_by_author(books)


if __name__ == "__main__":
    menu()