from flask import Blueprint, jsonify

electronics_bp = Blueprint('electronics', __name__)

# Sample data for electronics
electronics = [
    {"id": 1, "name": "Smartphone", "brand": "Brand A", "price": 299.99},
    {"id": 2, "name": "Laptop", "brand": "Brand B", "price": 799.99},
]

@electronics_bp.route('/electronics', methods=['GET'])
def get_electronics():
    return jsonify(electronics), 200
