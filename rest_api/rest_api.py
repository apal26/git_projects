from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

# In a real application, this would be a database
items = {
  1: {"name": "Apple"},
  2: {"name": "Banana"},
  3: {"name": "Orange"},
}
next_id = 4  # To assign new IDs for new items

@app.route('/items', methods=['GET'])
def get_items():
    """Retrieves all items."""
    return jsonify(items)

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Retrieves a single item by its ID."""
    item = items.get(item_id)
    if item:
        return jsonify(item)
    return jsonify({"message": "Item not found"}), 404

@app.route('/items', methods=['POST'])
def create_item():
    """Creates a new item."""
    global next_id
    data = request.json
    if not data or 'name' not in data:
        return jsonify({"message": "Name is required"}), 400
    new_item = {"name": data['name']}
    items[next_id] = new_item
    next_id += 1
    return jsonify(new_item), 201


if __name__ == '__main__':
    app.run(debug=True)
