# Library Management System

A command-line library management application built with Python. The application allows users to manage books, search the collection, and record borrowing and returning operations.

## Features

- Add books to the library collection.
- View all registered books.
- Search for books by title or author.
- Borrow available books.
- Return borrowed books.
- View currently borrowed books.
- Validate user input and handle empty-library scenarios.

## Requirements

- Python 3.10 or later
- Poetry

## Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:

   ```bash
   cd <project-directory>
   ```

3. Install project dependencies:

   ```bash
   poetry install
   ```

4. Run the application:

   ```bash
   poetry run python main.py
   ```

   Replace `main.py` if your main application file has a different name.

## Usage

When the application starts, the main menu is displayed:

```text
=================================
          LIBRARY MENU
=================================
1. Add a book
2. View all books
3. Search for a book
4. Borrow a book
5. Return a book
6. View borrowed books
7. Quit
=================================
Enter your choice (1-7):
```

Enter the number corresponding to the operation you want to perform and follow the prompts.

### Example: Searching for a book

```text
Enter your choice (1-7): 3
Enter a title or author to search for: Python

[1] Python Basics written by John Smith
    and published on 2024-01-15
```

*Example output for illustration; actual results depend on the books in your collection.*

### Example: Borrowing a book

Select option `4` and follow the prompts to identify the book and borrower.

The application checks whether a book is available before recording the borrowing operation.

### Example: Returning a book

Select option `5` and provide the requested book details to record its return.

### Viewing borrowed books

Select option `6` to view books that are currently borrowed. If no books are borrowed, the application displays a message indicating that the collection has no active borrowings.

## Project Structure

```text
library-management-system/
├── main.py       # Main menu and application flow
├── book.py       # Book class and book-related operations
├── borrower.py   # Borrowing and returning operations
├── utils.py      # Reusable input validation functions
├── pyproject.toml
├── poetry.lock
└── README.md
```

The project is organised into modules, with each module responsible for a particular part of the application.

- **main.py:** Coordinates user interaction and routes menu choices to the appropriate functions.
- **book.py:** Defines book-related functionality, including adding, viewing, searching, and filtering books.
- **borrower.py:** Handles borrowing and returning books.
- **utils.py:** Provides reusable functions for validating menu choices and text input.

## Concepts Demonstrated

- Python classes and objects
- Object-oriented programming
- Functions and modular programming
- Dictionaries and collection management
- Loops and conditional statements
- Input validation and exception handling
- Importing and reusing code across modules

## Current Limitations

- The application runs in the terminal and does not have a graphical interface.
- Data persistence depends on the implementation in the project modules. If records are held only in memory, they will not survive application restarts.
- The application is designed as a learning project rather than a production library system.

## Future Improvements

- Persist book and borrowing records using JSON or a database.
- Add automated tests for book management and borrowing operations.
- Improve search and record identification using unique book IDs.
- Introduce more robust data validation and error handling.
