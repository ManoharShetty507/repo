from flask import Flask, jsonify

app = Flask(__name__)

# Sample data for electronics
electronics = [
    {"id": 1, "name": "Laptop", "brand": "Dell", "price": 899.99},
    {"id": 2, "name": "Smartphone", "brand": "Samsung", "price": 499.99},
]

@app.route('/electronics', methods=['GET'])
def get_electronics():
    return jsonify(electronics), 200

if __name__ == "__main__":
    app.run(port=5002)
