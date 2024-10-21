from flask import Blueprint, jsonify

household_bp = Blueprint('household', __name__)

# Sample data for household items
household_items = [
    {"id": 1, "name": "Vacuum Cleaner", "brand": "Brand X", "price": 149.99},
    {"id": 2, "name": "Dishwasher", "brand": "Brand Y", "price": 499.99},
]

@household_bp.route('/household', methods=['GET'])
def get_household():
    return jsonify(household_items), 200
