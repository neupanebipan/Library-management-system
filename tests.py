import unittest
import json
from flask import Flask
from models import db, User, Book, BookDetails, BorrowedBooks
from routes import app
from datetime import date 

class TestLibraryManagementSystemAPI(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        client = app.test_client()

        # Test creating a new user
        user_data = {"Name": "John Doe", "Email": "john@example.com", "MembershipDate": "2023-01-01"}
        response = client.post('/users', json=user_data)
        self.assertEqual(response.status_code, 201)

        # Test getting the created user by ID
        created_user_id = json.loads(response.data)['UserID']
        response = client.get(f'/users/{created_user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['Name'], "John Doe")

    def test_list_all_users(self):
        client = app.test_client()

        # Test listing all users (empty initially)
        response = client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])

        # Test creating a user and then listing all users
        user_data = {"Name": "Jane Doe", "Email": "jane@example.com", "MembershipDate": "2023-01-02"}
        client.post('/users', json=user_data)
        response = client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data)), 1)
    
    def test_add_new_book(self):
        client = app.test_client()

        # Test adding a new book
        book_data = {"Title": "Sample Book", "ISBN": "1234567890", "PublishedDate": "2023-01-01", "Genre": "Fiction"}
        response = client.post('/books', json=book_data)
        self.assertEqual(response.status_code, 201)

        # Test getting the added book by ID
        created_book_id = json.loads(response.data)['BookID']
        response = client.get(f'/books/{created_book_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['Title'], "Sample Book")
    
    def test_list_all_books(self):
        client = app.test_client()

        # Test listing all books (empty initially)
        response = client.get('/books')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])

        # Test adding a book and then listing all books
        book_data = {"Title": "Another Book", "ISBN": "0987654321", "PublishedDate": "2023-01-02", "Genre": "Non-Fiction"}
        client.post('/books', json=book_data)
        response = client.get('/books')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data)), 1)
    
    def test_get_book_by_id(self):
        client = app.test_client()

        # Test getting a non-existent book by ID
        response = client.get('/books/999')
        self.assertEqual(response.status_code, 404)

        # Test adding a book and then getting it by ID
        book_data = {"Title": "Test Book", "ISBN": "1112223334", "PublishedDate": "2023-01-03", "Genre": "Science"}
        response = client.post('/books', json=book_data)
        created_book_id = json.loads(response.data)['BookID']

        response = client.get(f'/books/{created_book_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['Title'], "Test Book")


 

    def test_assign_update_book_details(self):      
        client = app.test_client()

        # Test assigning book details
        book_data = {"Title": "Details Book", "ISBN": "5555555555", "PublishedDate": "2023-01-04", "Genre": "Mystery"}
        response = client.post('/books', json=book_data)
        created_book_id = json.loads(response.data)['BookID']

        details_data = {"NumberOfPages": 200, "Publisher": "Sample Publisher", "Language": "English"}
        response = client.post(f'/books/{created_book_id}/details', json=details_data)
        self.assertEqual(response.status_code, 201)

        # Test updating book details
        updated_details_data = {"NumberOfPages": 250, "Publisher": "Updated Publisher", "Language": "Updated Language"}
        response = client.put(f'/books/{created_book_id}/details', json=updated_details_data)
        self.assertEqual(response.status_code, 200)

        # Test getting book details after update
        response = client.get(f'/books/{created_book_id}')
        self.assertEqual(response.status_code, 200)
              
        book_data = json.loads(response.data).get('book', {})
        self.assertIsNotNone(book_data, "Book details not found in the response")

        # Check specific details if 'book' is present
        if book_data:
            book_details = book_data.get('book_details')
            self.assertIsNotNone(book_details, "Book details not found in the response")

            # Check specific details if 'book_details' is present
            if book_details:
                self.assertEqual(book_details.get('NumberOfPages'), 250)
                self.assertEqual(book_details.get('Publisher'), "Updated Publisher")
                self.assertEqual(book_details.get('Language'), "Updated Language")

    def test_borrow_book(self):
        with app.app_context():
            client = app.test_client()

        # Create a user and a book for testing
        user_data = {"Name": "Test User", "Email": "test@example.com", "MembershipDate": date.today()}
        response_user = client.post('/users', json=user_data)
        user_id = json.loads(response_user.data)['UserID']

        book_data = {"Title": "Test Book", "ISBN": "1234567890", "PublishedDate": date.today(), "Genre": "Test Genre"}
        response_book = client.post('/books', json=book_data)
        book_id = json.loads(response_book.data)['BookID']

        # Borrow the book
        borrow_data = {"UserID": user_id, "BookID": book_id, "BorrowDate": date.today(), "ReturnDate": date.today()}
        response_borrow = client.post('/borrow', json=borrow_data)
        self.assertEqual(response_borrow.status_code, 201)

        # Check if the book was borrowed successfully
        with app.test_request_context():
            borrowed_books = BorrowedBooks.query.filter_by(UserID=user_id, BookID=book_id).all()
            self.assertEqual(len(borrowed_books), 1)
   
    def test_return_book(self):
        with app.app_context():
            client = app.test_client()

        # Create a user and a book for testing
        user_data = {"Name": "Test User", "Email": "test@example.com", "MembershipDate": date.today()}
        response_user = client.post('/users', json=user_data)
        user_id = json.loads(response_user.data)['UserID']

        book_data = {"Title": "Test Book", "ISBN": "1234567890", "PublishedDate": date.today(), "Genre": "Test Genre"}
        response_book = client.post('/books', json=book_data)
        book_id = json.loads(response_book.data)['BookID']

        # Borrow the book
        borrow_data = {"UserID": user_id, "BookID": book_id, "BorrowDate": date.today(), "ReturnDate": date.today()}
        response_borrow = client.post('/borrow', json=borrow_data)
        self.assertEqual(response_borrow.status_code, 201)

        # Return the book
        response_return = client.put(f'/return/{user_id}/{book_id}')
        self.assertEqual(response_return.status_code, 200)

        # Check if the book was returned successfully
        with app.test_request_context():
            borrowed_book = BorrowedBooks.query.filter_by(UserID=user_id, BookID=book_id).first()
            self.assertIsNotNone(borrowed_book.ReturnDate)






    # Similar test methods can be added for other endpoints (e.g., test_add_new_book, test_list_all_books, etc.)

if __name__ == '__main__':
    unittest.main()
