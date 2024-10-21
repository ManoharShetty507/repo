from flask import Flask, jsonify

app = Flask(__name__)

# Sample data for household items
household_items = [
    {"id": 1, "name": "Vacuum Cleaner", "brand": "Dyson", "price": 299.99},
    {"id": 2, "name": "Air Purifier", "brand": "Philips", "price": 149.99},
]

@app.route('/household', methods=['GET'])
def get_household_items():
    return jsonify(household_items), 200

if __name__ == "__main__":
    app.run(port=5003)
