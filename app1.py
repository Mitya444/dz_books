from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)


class LiteraryFormat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    books = db.relationship('Book', backref='format', lazy=True)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    literary_format_id = db.Column(db.Integer, db.ForeignKey('literary_format.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)


@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    output = []
    for book in books:
        output.append({
            'id': book.id,
            'title': book.title,
            'author': book.author.name,
            'literary_format': book.format.name
        })
    return jsonify({'books': output})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
