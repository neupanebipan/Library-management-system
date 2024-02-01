from flask import Flask, request, jsonify
from models import db, User, Book, BookDetails, BorrowedBooks

app = Flask(__name__)

# Set up the database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/library-management-system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the Flask extension
db.init_app(app)

# Create tables (if not already created)
with app.app_context():
    try:
        db.create_all()
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")

# User APIs
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully", "UserID": new_user.UserID}), 201

@app.route('/users', methods=['GET'])
def list_all_users():
    users = User.query.all()
    users_data = [{"UserID": user.UserID, "Name": user.Name, "Email": user.Email, "MembershipDate": user.MembershipDate} for user in users]
    return jsonify(users_data)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        user_data = {"UserID": user.UserID, "Name": user.Name, "Email": user.Email, "MembershipDate": user.MembershipDate}
        return jsonify(user_data)
    else:
        return jsonify({"message": "User not found"}), 404

# Book APIs
@app.route('/books', methods=['POST'])
def add_new_book():
    data = request.get_json()
    new_book = Book(**data)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added successfully","BookID":new_book.BookID}), 201

@app.route('/books', methods=['GET'])
def list_all_books():
    books = Book.query.all()
    books_data = [{"BookID": book.BookID, "Title": book.Title, "ISBN": book.ISBN, "PublishedDate": book.PublishedDate, "Genre": book.Genre} for book in books]
    return jsonify(books_data)

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    book = Book.query.get(book_id)
    if book:
        book_data = {"BookID": book.BookID, "Title": book.Title, "ISBN": book.ISBN, "PublishedDate": book.PublishedDate, "Genre": book.Genre}
        return jsonify(book_data)
    else:
        return jsonify({"message": "Book not found"}), 404

@app.route('/books/<int:book_id>/details', methods=['POST', 'PUT'])
def assign_update_book_details(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    if request.method == 'POST':
        data = request.get_json()
        new_details = BookDetails(**data, BookID=book_id)
        db.session.add(new_details)
        db.session.commit()
        return jsonify({"message": "Book details added successfully"}), 201
    elif request.method == 'PUT':
        data = request.get_json()
        book_details = BookDetails.query.filter_by(BookID=book_id).first()
        if book_details:
            for key, value in data.items():
                setattr(book_details, key, value)
            db.session.commit()
            return jsonify({"message": "Book details updated successfully"})
        else:
            return jsonify({"message": "Book details not found"}), 404

# BorrowedBooks APIs
@app.route('/borrow', methods=['POST'])
def borrow_book():
    data = request.get_json()
    borrowed_book = BorrowedBooks(**data)
    db.session.add(borrowed_book)
    db.session.commit()
    return jsonify({"message": "Book borrowed successfully"}), 201

@app.route('/return/<int:user_id>/<int:book_id>', methods=['PUT'])
def return_book(user_id, book_id):
    borrowed_book = BorrowedBooks.query.filter_by(UserID=user_id, BookID=book_id).first()
    if borrowed_book:
        # Logic for returning the book
        borrowed_book.returned = True  
        db.session.commit()
        return jsonify({"message": "Book returned successfully"}), 200
    else:
        return jsonify({"message": "Borrowed book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
