from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

app = Flask(__name__)

CORS(app)

# MongoDB connection
client = MongoClient("mongodb+srv://shoaib:shoaibmansuri@cluster0.zghdsdl.mongodb.net/?retryWrites=true&w=majority")
db = client["<Zomato_db>"]
dishes_collection = db["dishes"]
orders_collection = db["orders"]



@app.route('/bah')
def index():
    menu_data = list(orders_collection.find())
    menu_data = json.loads(json.dumps(orders_collection, default=str))
    return menu_data



@app.route('/review_orders')
def review_orders():
    orders_data = list(orders_collection.find())
    orders_data = json.loads(json.dumps(orders_data, default=str))
    return orders_data



@app.route('/')
def review_order():
    orders_data = list(dishes_collection.find())
    orders_data = json.loads(json.dumps(dishes_collection, default=str))
    return orders_data



@app.route('/add_dish', methods=['POST'])
def add_dish():
    data = request.get_json()
    dish_name = data['name']
    dish_price = float(data['price'])
    dish_availability = True if data.get('availability') else False

    dish = {
        "name": dish_name,
        "price": dish_price,
        "availability": dish_availability
    }

    dishes_collection.insert_one(dish)

    return jsonify(success=True)


@app.route('/dishes/<string:dish_id>', methods=['PATCH'])
def update_availability(dish_id):
    data = request.get_json()
    availability = data.get('availability')

    result = dishes_collection.update_one(
        {"_id": ObjectId(dish_id)},
        {"$set": {"availability": availability}}
    )

    if result.modified_count == 1:
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Failed to update the dish availability.")


@app.route('/take_order', methods=['POST'])
def take_order():
    data = request.get_json()
    customer_name = data['customer_name']
    dish_ids = [data['dish_ids']] if isinstance(data['dish_ids'], int) else data['dish_ids']

    for dish_id in dish_ids:
        dish = dishes_collection.find_one({"_id": ObjectId(dish_id)})
        if dish is None or not dish['availability']:
            return jsonify(success=False, message="Sorry, the requested dish is not available.")

    order = {
        "customer_name": customer_name,
        "dish_ids": [ObjectId(dish_id) for dish_id in dish_ids],
        "status": data['status']
    }

    orders_collection.insert_one(order)

    return jsonify(success=True)


@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    data = request.get_json()
    order_id = data['id']
    status = data['status']

    result = orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": status}}
    )

    if result.modified_count == 1:
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Failed to update the order status.")





@app.route('/remove_dish/<string:dish_id>', methods=['DELETE'])
def remove_dish(dish_id):
    result = dishes_collection.delete_one({"_id": ObjectId(dish_id)})

    if result.deleted_count == 1:
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Failed to remove the dish.")


if __name__ == '__main__':
    app.run(debug=True)
