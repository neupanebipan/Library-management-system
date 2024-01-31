import datetime
import pytest
from flask import json
from routes import app 
from models import BookDetails, BorrowedBooks, db, User, Book
from flask_jwt_extended import create_access_token

@pytest.fixture(scope='module')
def test_app():
    """Create and configure a new app instance for each test."""
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Use an in-memory SQLite database for tests
        "JWT_SECRET_KEY": "50ddbf616eb3ee3d"  # Set JWT secret key for testing
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def test_client(test_app):
    """A test test_client for the app."""
    test_client = test_app.test_client()
    with test_app.app_context():
        yield test_client
        db.session.rollback()
        db.session.query(User).delete()
        db.session.query(Book).delete()
        db.session.query(BookDetails).delete()
        db.session.query(BorrowedBooks).delete()
        db.session.commit()

@pytest.fixture(scope="function")
def setup_test_data(test_client):
    """Setup test data for the database."""
    with test_client.application.app_context():
        db.session.rollback()
        db.session.query(User).delete()
        db.session.query(Book).delete()
        db.session.query(BookDetails).delete()
        db.session.query(BorrowedBooks).delete()

        user = User(Name='Test User', Email='test@example.com', MembershipDate=datetime.datetime.utcnow(), PasswordHash='testpass')
        book = Book(Title='Test Book', ISBN='123-4567890123', PublishedDate=datetime.datetime.utcnow().date(), Genre='Test Genre')
        db.session.add(user)
        db.session.add(book)
        db.session.commit()

        yield user.UserID  # Return the created user ID
   

def get_auth_token(test_client, email='test@example.com'):
    """Generate a JWT token for authentication."""
    access_token = create_access_token(identity=email)
    return f'Bearer {access_token}'

def test_add_user(test_client):
    """Test adding a new user."""
    new_user = {
        'Name': 'Test User',
        'Email': 'test@example.com',
        'MembershipDate': datetime.datetime.utcnow().isoformat(),
        'PasswordHash': 'testpass'
    }
    response = test_client.post('/user/create', json=new_user)
    assert response.status_code == 201
    assert b"User created successfully" in response.data

def test_update_user(test_client, setup_test_data):
    auth_token = get_auth_token(test_client)
    headers = {'Authorization': auth_token}
    
    data = {'Name': 'Updated User'}
    response = test_client.put(f'/user/{setup_test_data}', json=data, headers=headers)
    assert response.status_code == 200
    assert b'User updated successfully' in response.data

def test_delete_user(test_client, setup_test_data):
    auth_token = get_auth_token(test_client)
    headers = {'Authorization': auth_token}

    response = test_client.delete(f'/user/{setup_test_data}', headers=headers)
    assert response.status_code == 200
    assert b'User deleted successfully' in response.data

# Test CRUD operations for Book
def test_add_book(test_client):
    new_book = {
        'Title': 'Test Book',
        'ISBN': '123-4567890123',
        'PublishedDate': datetime.datetime.utcnow().isoformat(),
        'Genre': 'Test Genre'
    }
    response = test_client.post('/book/create', json=new_book)
    assert response.status_code == 201
    assert b"Book added successfully" in response.data

def test_update_book(test_client, setup_test_data):
    auth_token = get_auth_token(test_client)
    headers = {'Authorization': auth_token}
    
    data = {'Title': 'Updated Book'}
    response = test_client.put(f'/book/{setup_test_data}', json=data, headers=headers)
    assert response.status_code == 200
    assert b'Book updated successfully' in response.data

def test_delete_book(test_client, setup_test_data):
    auth_token = get_auth_token(test_client)
    headers = {'Authorization': auth_token}

    response = test_client.delete(f'/book/{setup_test_data}', headers=headers)
    assert response.status_code == 200
    assert b'Book deleted successfully' in response.data

# Test CRUD operations for BookDetails
def test_assign_update_book_details(test_client, setup_test_data):
    auth_token = get_auth_token(test_client)
    headers = {'Authorization': auth_token}
    
    data = {
        'NumberOfPages': 200,
        'Publisher': 'Test Publisher',
        'Language': 'English'
    }

    response = test_client.put(f'/book/details/{setup_test_data}', json=data, headers=headers)
    assert response.status_code == 200
    assert b'Book details assigned/updated successfully' in response.data

# Test CRUD operations for BorrowedBooks
def test_borrow_book(test_client, setup_test_data):
    auth_token = get_auth_token(test_client)
    headers = {'Authorization': auth_token}

    # Replace these values with valid ones from your test data
    user_id, book_id = setup_test_data


    data = {
        'UserID': user_id,
        'BookID': book_id,
        'BorrowDate': datetime.datetime.utcnow().isoformat()
    }

    response = test_client.post('/borrow_book', json=data, headers=headers)
    assert response.status_code == 201
    assert b'Book borrowed successfully' in response.data

def test_return_book(test_client, setup_test_data):
    auth_token = get_auth_token(test_client)
    headers = {'Authorization': auth_token}

    response = test_client.put(f'/return_book/{setup_test_data}', headers=headers)
    assert response.status_code == 200
    assert b'Book returned successfully' in response.data

# Test authentication
def test_unauthenticated_access(test_client):
    response = test_client.get('/user/list')
    assert response.status_code == 401
    assert b"Missing Authorization Header" in response.data

def test_invalid_token(test_client):
    headers = {'Authorization': 'Bearer invalid_token'}
    response = test_client.get('/user/list', headers=headers)
    assert response.status_code == 422
    assert b"Not enough segments" in response.data


def test_get_user_by_id(test_client, setup_test_data):
    """Test getting a user by ID."""
    auth_token = get_auth_token(test_client)
    headers = {'Authorization': auth_token}
    
    response = test_client.get(f'/user/{setup_test_data}', headers=headers)
    assert response.status_code == 200
    assert b"Test User" in response.data

def test_list_users(test_client, setup_test_data):
    """Test listing users."""
    auth_token = get_auth_token(test_client)
    headers = {'Authorization': auth_token}
    
    response = test_client.get('/user/list', headers=headers)
    assert response.status_code == 200
    assert b'Test User' in response.data


def test_add_book(test_client):
    """Test adding a book."""
    auth_token = get_auth_token(test_client)
    headers = {'Authorization': auth_token}
    
    data = {'Title': 'Test Book', 'ISBN': '1234567890', 'PublishedDate': '2023-01-01', 'Genre': 'Fiction'}
    response = test_client.post('/book/create', data=json.dumps(data), content_type='application/json', headers=headers)
    assert response.status_code == 201
    assert b'Book added successfully' in response.data

def test_list_books(test_client, setup_test_data):
    """Test listing books."""
    auth_token = get_auth_token(test_client)
    headers = {'Authorization': auth_token}
    
    response = test_client.get('/book/list', headers=headers)
    assert response.status_code == 200
    assert b'Test Book' in response.data

def test_get_book(test_client, setup_test_data):
    """Test getting a book by ID."""
    auth_token = get_auth_token(test_client)
    headers = {'Authorization': auth_token}
    
    response = test_client.get('/book/1', headers=headers)
    assert response.status_code == 200
    assert b'Test Book' in response.data

def test_assign_update_book_details(test_client, setup_test_data):
    """Test assigning or updating book details."""
    auth_token = get_auth_token(test_client)
    headers = {'Authorization': auth_token}
    
    data = {
        'NumberOfPages': 200,
        'Publisher': 'Test Publisher',
        'Language': 'English'
    }

    response = test_client.put(f'/book/details/{setup_test_data}', data=json.dumps(data), content_type='application/json', headers=headers)
    assert response.status_code == 200
    assert b'Book details assigned/updated successfully' in response.data



if __name__ == '__main__':
    pytest.main()




