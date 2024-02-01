
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    MembershipDate = db.Column(db.Date, nullable=False)
    
    
    # Relationships
    borrowed_books = db.relationship('BorrowedBooks', backref='user', lazy=True)

class Book(db.Model):
    __tablename__ = 'book'

    BookID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    ISBN = db.Column(db.String(20), unique=True, nullable=False)
    PublishedDate = db.Column(db.Date, nullable=False)
    Genre = db.Column(db.String(50), nullable=False)

    # Relationships
    book_details = db.relationship('BookDetails', backref='book', uselist=False)

class BookDetails(db.Model):
    __tablename__ = 'bookdetails'

    DetailsID = db.Column(db.Integer, primary_key=True)
    BookID = db.Column(db.Integer, db.ForeignKey('book.BookID'), unique=True, nullable=False)
    NumberOfPages = db.Column(db.Integer, nullable=False)
    Publisher = db.Column(db.String(100), nullable=False)
    Language = db.Column(db.String(50), nullable=False)

class BorrowedBooks(db.Model):
    __tablename__ = 'borrowedbooks'

    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), primary_key=True)
    BookID = db.Column(db.Integer, db.ForeignKey('book.BookID'), primary_key=True)
    BorrowDate = db.Column(db.Date, nullable=False)
    ReturnDate = db.Column(db.Date)
    
 


