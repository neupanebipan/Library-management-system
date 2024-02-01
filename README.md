## Library Management System
The Library Management System is a Flask-based web application designed to manage a library's book inventory, user information, and borrowing history. This README provides an overview of the project structure, functionalities, and instructions for setting up and running the application.
### Table of Contents
- [Project Overview](#project-overview)
- [Database Schema Design](#database-schema-design)
- [API Development](#api-development)
- [Testing and Validation](#testing-and-validation)
- [Code Quality and Error Handling](#code-quality-and-error-handling)
- [Project Setup](#project-setup)
  - [Requirements](#requirements)
  - [Setting Up a Virtual Environment](#setting-up-a-virtual-environment)
  - [Database Setup](#database-setup)
  - [Installation](#installation)
  - [How to Run](#how-to-run)

## Project Overview

The Library Management System is organized around the following models:

### User Model

- **Attributes:** UserID, Name, Email, MembershipDate
- **Relationships:** 1-M with BorrowedBooks (A user can borrow multiple books)

### Book Model

- **Attributes:** BookID, Title, ISBN, PublishedDate, Genre
- **Relationships:** 1-1 with BookDetails (Each book has one set of details)

### BookDetails Model (for 1-1 relationship)

- **Attributes:** DetailsID, BookID (FK), NumberOfPages, Publisher, Language
- **Relationships:** 1-1 with Book (Each set of book details is linked to exactly one book)

### BorrowedBooks Model (to demonstrate 1-N relationship)

- **Attributes:** UserID (FK), BookID (FK), BorrowDate, ReturnDate
- **Relationships:** 1-M with User (A user can borrow multiple books)


## Database Schema Design

The database schema is designed to establish relationships between users, books, book details, and borrowed books, providing a comprehensive solution for library management.

## API Development

The Flask application includes the following APIs for each model:

### User APIs

- **Create a New User:** Endpoint to add a new user to the system with details like name, email, and membership date.
- **List All Users:** Endpoint to retrieve a list of all users in the system.
- **Get User by ID:** Endpoint to fetch a user's details using their UserID.

### Book APIs

- **Add a New Book:** Endpoint to add a new book record, including title, ISBN, published date, and genre.
- **List All Books:** Endpoint to retrieve a list of all books in the library.
- **Get Book by ID:** Endpoint to fetch details of a specific book using its BookID.
- **Assign/Update Book Details:** Endpoint to assign details to a book or update existing book details, like the number of pages, publisher, language.

### BorrowedBooks APIs

- **Borrow a Book:** Endpoint to record the borrowing of a book by linking a user with a book.
- **Return a Book:** Endpoint to update the system when a book is returned.
- **List All Borrowed Books:** Endpoint to list all books currently borrowed from the library.

## Testing and Validation

The application includes a suite of unit tests to ensure each API's functionality and reliability. CRUD operations are thoroughly tested for each model.

## Code Quality and Error Handling

The codebase is structured for readability and is well-documented. Robust error handling is implemented to cover edge cases and potential errors during API interactions.

## Authentication Implementation (Bonus)

As a bonus challenge, the implementation of user authentication is pending. Future updates may include securing the APIs with appropriate authentication mechanisms.

## Project Setup

### Requirements

- Flask
- PostgreSQL

### Installation

1. Clone the repository: `git clone https://github.com/neupanebipan/Library-management-system`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up PostgreSQL database: [Database setup](#dbasesetup)


### How to Run

1. Navigate to the project directory.
2. Run the Flask application: `python routes.py`
3. Access the application at http://localhost:5000
4. Run the tests for API endpoints:`pytest tests.py`
## Setting Up a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies. Follow these steps to set up a virtual environment:
##### Create a virtual environment (you can use 'venv' or 'virtualenv')
`python -m venv venv`
##### Activate the virtual environment
##### On Windows
`venv\Scripts\activate`
##### On macOS/Linux
`source venv/bin/activate`
## Database Setup

This project uses PostgreSQL as the database. Follow these steps to set up the database:

1. Create a PostgreSQL database for the project.
2. Apply the database migrations using the following commands:

```bash
# Run migrations
flask db init
flask db migrate
flask db upgrade


