import json
import os
from abc import ABC
from datetime import date, datetime
from book import Book 
from utils import get_choice, get_text
from book import add_book, books, read_all_books, search_book, filter_borrowed_books
from borrower import return_book, borrow_book





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
            "7. Quit\n"
            "=================================\n"
            "Enter your choice (1-7): ",
            range(1, 8),
        )
        if choice == 1:
            add_book()
        elif choice == 7:
            print("Goodbye!")
            break
        elif not books:
            print("There are no books in the library yet. Add a book first.")
        elif choice == 2:
            read_all_books()
        elif choice == 3:
            search_book(get_text("Enter a title or author to search for: "))
        elif choice == 4:
            borrow_book()
        elif choice == 5:
            return_book()
        elif choice == 6:
            if any(book.status for book in books.values()):
                filter_borrowed_books()
            else:
                print("No books are currently borrowed.")



menu()