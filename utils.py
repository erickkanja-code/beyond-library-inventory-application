import json
import os
from abc import ABC
from datetime import date, datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKS_FILE = os.path.join(BASE_DIR, "books.json")
BORROW_TRANSACTIONS_FILE = os.path.join(BASE_DIR, "borrow_transactions.json")

def get_text(prompt):
    """Keep asking until the user enters a non-empty value.

    Args:
        prompt (str): The message shown to the user.

    Returns:
        str: The text entered, with surrounding spaces removed.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def get_int(prompt):
    """Keep asking until the user enters a whole number.

    Args:
        prompt (str): The message shown to the user.

    Returns:
        int: The number entered.
    """
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_choice(prompt, options):
    """Keep asking until the user enters a number that is one of the options.

    Args:
        prompt (str): The message shown to the user.
        options (iterable of int): The numbers that are accepted.

    Returns:
        int: The accepted number entered by the user.
    """
    options = list(options)
    while True:
        number = get_int(prompt)
        if number in options:
            return number
        print(f"Invalid choice. Please enter one of: {', '.join(str(o) for o in options)}.")


def get_date(prompt):
    """Keep asking until the user enters a real date in MM-DD-YYYY format.

    Args:
        prompt (str): The message shown to the user.

    Returns:
        str: The date written as MM-DD-YYYY.
    """
    while True:
        value = input(prompt).strip()
        try:
            return datetime.strptime(value, "%m-%d-%Y").strftime("%m-%d-%Y")
        except ValueError:
            print("Invalid date. Use MM-DD-YYYY, for example 08-01-1965.")


def get_phone(prompt):
    """Keep asking until the user enters a valid phone number.

    A valid number has 9 to 15 digits and may start with a plus sign.

    Args:
        prompt (str): The message shown to the user.

    Returns:
        str: The phone number entered.
    """
    while True:
        value = input(prompt).strip()
        digits = value[1:] if value.startswith("+") else value
        if digits.isdigit() and 9 <= len(digits) <= 15:
            return value
        print("Invalid phone number. Enter 9 to 15 digits, for example 0788123456.")
