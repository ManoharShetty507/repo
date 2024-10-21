from flask import Flask, jsonify

app = Flask(__name__)

# Sample data for books
books = [
    {"id": 1, "title": "1984", "author": "George Orwell", "price": 12.99},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "price": 10.99},
]

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books), 200

if __name__ == "__main__":
    app.run(port=5001)
