from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy data
dishes =  [
    {"id": 1, "name": "Pizza", "price": 299.99, "availability": True},
    {"id": 2, "name": "Burger", "price": 249.99, "availability": True},
    {"id": 3, "name": "Pasta", "price": 219.99, "availability": False},
    {"id": 4, "name": "Salad", "price": 249.99, "availability": True},
    {"id": 5, "name": "Sushi", "price": 329.99, "availability": True},
    {"id": 6, "name": "Steak", "price": 349.99, "availability": False},
    {"id": 7, "name": "Sandwich", "price": 229.99, "availability": True},
    {"id": 8, "name": "Soup", "price": 209.99, "availability": True},
    {"id": 9, "name": "Chicken Wings", "price": 289.99, "availability": True},
    {"id": 10, "name": "Fish and Chips", "price": 249.99, "availability": False},
    {"id": 11, "name": "Ice Cream", "price": 209.99, "availability": True},
    {"id": 12, "name": "Pancakes", "price": 239.99, "availability": True}
]

orders = []


@app.route('/')
def index():
    return jsonify(dishes=dishes, orders=orders)


@app.route('/add_dish', methods=['POST'])
def add_dish():
    data = request.get_json()
    dish_name = data['name']
    dish_price = float(data['price'])
    dish_availability = True if data.get('availability') else False

    dish_id = len(dishes) + 1
    dish = {"id": dish_id, "name": dish_name, "price": dish_price, "availability": dish_availability}
    dishes.append(dish)

    return jsonify(success=True)


@app.route('/dishes/<int:dish_id>', methods=['PATCH'])
def update_availability(dish_id):
    availability = request.get_json().get('availability')

    for dish in dishes:
        if dish['id'] == dish_id:
            dish['availability'] = True if availability else False
            break

    return jsonify(success=True)


@app.route('/take_order', methods=['POST'])
def take_order():
    data = request.get_json()
    customer_name = data['customer_name']
    dish_ids = [data['dish_ids']] if isinstance(data['dish_ids'], int) else data['dish_ids']

    for dish_id in dish_ids:
        dish = next((item for item in dishes if item['id'] == dish_id), None)
        if dish is None or not dish['availability']:
            return jsonify(success=False, message="Sorry, the requested dish is not available.")

    order_id = len(orders) + 1
    order = {"id": data['id'], "customer_name": customer_name, "dish_ids": dish_ids, "status": data['status']}
    orders.append(order)

    return jsonify(success=True)


@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    data = request.get_json()
    order_id = int(data['order_id'])
    status = data['status']

    for order in orders:
        if order['id'] == order_id:
            order['status'] = status
            break

    return jsonify(success=True)


@app.route('/review_orders')
def review_orders():
    return jsonify(orders=orders)


@app.route('/remove_dish/<int:dish_id>', methods=['DELETE'])
def remove_dish(dish_id):
    global dishes

    dishes = [dish for dish in dishes if dish['id'] != dish_id]

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
