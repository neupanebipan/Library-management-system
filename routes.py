from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from models import db, User, Book, BookDetails, BorrowedBooks
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/lib_mgmt_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '50ddbf616eb3ee3d'

jwt = JWTManager(app)
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# User APIs
@app.route('/user/create', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/user/list', methods=['GET'])
@jwt_required() 
def list_users():
    users = User.query.all()
    users_data = [{'UserID': user.UserID, 'Name': user.Name, 'Email': user.Email, 'MembershipDate': user.MembershipDate} for user in users]
    return jsonify({'users': users_data})

@app.route('/user/<int:user_id>', methods=['GET'])
@jwt_required() 
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        user_data = {'UserID': user.UserID, 'Name': user.Name, 'Email': user.Email, 'MembershipDate': user.MembershipDate}
        return jsonify(user_data)
    return jsonify({'message': 'User not found'}), 404

@app.route('/user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.get_json()
        # Update user fields based on the data received
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

# Book APIs
@app.route('/book/create', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(**data)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201
@app.route('/book/<int:book_id>', methods=['PUT'])

def update_book(book_id):
    book = Book.query.get(book_id)
    if book:
        data = request.get_json()
        for key, value in data.items():
            setattr(book, key, value)
        db.session.commit()
        return jsonify({'message': 'Book updated successfully'}), 200
    else:
        return jsonify({'message': 'Book not found'}), 404

@app.route('/book/<int:book_id>', methods=['DELETE'])

def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'}), 200
    else:
        return jsonify({'message': 'Book not found'}), 404


@app.route('/book/list', methods=['GET'])
def list_books():
    books = Book.query.all()
    book_list = [{'BookID': book.BookID, 'Title': book.Title, 'ISBN': book.ISBN, 'PublishedDate': str(book.PublishedDate), 'Genre': book.Genre} for book in books]
    return jsonify({'books': book_list})

@app.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify({'BookID': book.BookID, 'Title': book.Title, 'ISBN': book.ISBN, 'PublishedDate': str(book.PublishedDate), 'Genre': book.Genre})
    else:
        return jsonify({'message': 'Book not found'}), 404

@app.route('/book/details/<int:book_id>', methods=['PUT'])
def assign_update_book_details(book_id):
    data = request.get_json()
    book = Book.query.get(book_id)
    if book:
        book_details = BookDetails.query.filter_by(Book_ID=book_id).first()
        if not book_details:
            # Create new BookDetails if it doesn't exist
            book_details = BookDetails(**data, Book_ID=book_id)
            db.session.add(book_details)
        else:
            # Update existing BookDetails
            for key, value in data.items():
                setattr(book_details, key, value)
        db.session.commit()
        return jsonify({'message': 'Book details assigned/updated successfully'})
    else:
        return jsonify({'message': 'Book not found'}), 404

# BorrowedBooks APIs
@app.route('/borrow_book', methods=['POST'])
def borrow_book():
    data = request.get_json()
    new_borrowed_book = BorrowedBooks(**data)
    db.session.add(new_borrowed_book)
    db.session.commit()
    return jsonify({'message': 'Book borrowed successfully'}), 201

@app.route('/return_book/<int:borrowed_id>', methods=['PUT'])
def return_book(borrowed_id):
    borrowed_book = BorrowedBooks.query.get(borrowed_id)
    if borrowed_book:
        borrowed_book.ReturnDate = db.func.current_date()
        db.session.commit()
        return jsonify({'message': 'Book returned successfully'})
    else:
        return jsonify({'message': 'Borrowed book not found'}), 404

@app.route('/borrowed_books/list', methods=['GET'])
def list_borrowed_books():
    borrowed_books = BorrowedBooks.query.all()
    borrowed_books_list = [{'BorrowedID': bb.BorrowedID, 'UserID': bb.UserID, 'BookID': bb.BookID, 'BorrowDate': str(bb.BorrowDate), 'ReturnDate': str(bb.ReturnDate) if bb.ReturnDate else None} for bb in borrowed_books]
    return jsonify({'borrowed_books': borrowed_books_list})

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    
    # Authenticate user
    user = User.query.filter_by(Email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

if __name__ == '__main__':
    app.run(debug=True)

