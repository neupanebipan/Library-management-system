from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user_table'
    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    MembershipDate = db.Column(db.Date, nullable=False)
    PasswordHash = db.Column(db.String(128))  

    def set_password(self, password):
        self.PasswordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.PasswordHash, password)

class Book(db.Model):
    __tablename__ = 'book'
    BookID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    ISBN = db.Column(db.String(20), nullable=False)
    PublishedDate = db.Column(db.Date, nullable=False)
    Genre = db.Column(db.String(50), nullable=False)

class BookDetails(db.Model):
    __tablename__ = 'book_details'
    DetailsID = db.Column(db.Integer, primary_key=True)
    Book_ID = db.Column(db.Integer, db.ForeignKey('book.BookID'), unique=True, nullable=False)
    NumberOfPages = db.Column(db.Integer, nullable=False)
    Publisher = db.Column(db.String(255), nullable=False)
    Language = db.Column(db.String(50), nullable=False)

class BorrowedBooks(db.Model):
    __tablename__ = 'borrowed_books'
    BorrowedID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user_table.UserID'), nullable=False)
    BookID = db.Column(db.Integer, db.ForeignKey('book.BookID'), nullable=False)
    BorrowDate = db.Column(db.Date, nullable=False)
    ReturnDate = db.Column(db.Date)
    
 


