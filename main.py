from flask import Flask, jsonify, request
from models import db, Product, Customer, Staff, Order
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'warehouse',
    'host': 'localhost',
    'port': 27017
}

db.init_app(app)

# Helper function for limit parameter
def apply_limit(cursor):
    limit = request.args.get('limit', type=int)
    if limit is not None:
        cursor = cursor.limit(limit)
    return cursor

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(415)
def unsupported_media_type(error):
    return jsonify({'error': 'Unsupported media type'}), 415

# Endpoints for Products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.objects()
    products = apply_limit(products)
    return jsonify(products)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        price=data['price'],
        amount=data['amount'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    new_product.save()
    return jsonify(new_product), 201

@app.route('/products/<string:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.objects(id=ObjectId(product_id)).first()
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product)

@app.route('/products/<string:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = Product.objects(id=ObjectId(product_id)).first()
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    product.update(
        price=data.get('price', product.price),
        amount=data.get('amount', product.amount),
        updated_at=datetime.utcnow()
    )
    product.reload()
    return jsonify(product)

@app.route('/products/<string:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.objects(id=ObjectId(product_id)).first()
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    product.delete()
    return '', 204

# Endpoints for Customers
@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.objects()
    customers = apply_limit(customers)
    return jsonify(customers)

@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    new_customer = Customer(
        first_name=data['first_name'],
        last_name=data['last_name'],
        street=data['street'],
        postal_code=data['postal_code'],
        age=data['age'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    new_customer.save()
    return jsonify(new_customer), 201

@app.route('/customers/<string:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.objects(id=ObjectId(customer_id)).first()
    if customer is None:
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify(customer)

@app.route('/customers/<string:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    customer = Customer.objects(id=ObjectId(customer_id)).first()
    if customer is None:
        return jsonify({'error': 'Customer not found'}), 404
    customer.update(
        age=data.get('age', customer.age),
        updated_at=datetime.utcnow()
    )
    customer.reload()
    return jsonify(customer)

@app.route('/customers/<string:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.objects(id=ObjectId(customer_id)).first()
    if customer is None:
        return jsonify({'error': 'Customer not found'}), 404
    customer.delete()
    return '', 204

# Endpoints for Staff
@app.route('/staff', methods=['GET'])
def get_staff():
    staff = Staff.objects()
    staff = apply_limit(staff)
    return jsonify(staff)

@app.route('/staff', methods=['POST'])
def add_staff():
    data = request.get_json()
    new_staff = Staff(
        first_name=data['first_name'],
        last_name=data['last_name'],
        employee_since=datetime.strptime(data['employee_since'], '%Y-%m-%d'),
        age=data['age'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    new_staff.save()
    return jsonify(new_staff), 201

@app.route('/staff/<string:staff_id>', methods=['GET'])
def get_staff_member(staff_id):
    staff_member = Staff.objects(id=ObjectId(staff_id)).first()
    if staff_member is None:
        return jsonify({'error': 'Staff member not found'}), 404
    return jsonify(staff_member)

@app.route('/staff/<string:staff_id>', methods=['PUT'])
def update_staff(staff_id):
    data = request.get_json()
    staff_member = Staff.objects(id=ObjectId(staff_id)).first()
    if staff_member is None:
        return jsonify({'error': 'Staff member not found'}), 404
    staff_member.update(
        last_name=data.get('last_name', staff_member.last_name),
        age=data.get('age', staff_member.age),
        updated_at=datetime.utcnow()
    )
    staff_member.reload()
    return jsonify(staff_member)

@app.route('/staff/<string:staff_id>', methods=['DELETE'])
def delete_staff(staff_id):
    staff_member = Staff.objects(id=ObjectId(staff_id)).first()
    if staff_member is None:
        return jsonify({'error': 'Staff member not found'}), 404
    staff_member.delete()
    return '', 204

# Endpoints for Orders
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.objects()
    orders = apply_limit(orders)
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def add_order():
    data = request.get_json()
    new_order = Order(
        product_id=Product.objects(id=ObjectId(data['product_id'])).first(),
        customer_id=Customer.objects(id=ObjectId(data['customer_id'])).first(),
        staff_id=Staff.objects(id=ObjectId(data['staff_id'])).first(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    new_order.save()
    return jsonify(new_order), 201

@app.route('/orders/<string:product_id>', methods=['GET'])
def get_order_by_product(product_id):
    orders = Order.objects(product_id=ObjectId(product_id))
    if not orders:
        return jsonify({'error': 'Orders not found for the given product'}), 404
    orders = apply_limit(orders)
    return jsonify(orders)

@app.route('/orders/<string:product_id>/<string:customer_id>', methods=['GET'])
def get_order_by_product_and_customer(product_id, customer_id):
    order = Order.objects(product_id=ObjectId(product_id), customer_id=ObjectId(customer_id)).first()
    if order is None:
        return jsonify({'error': 'Order not found for the given product and customer'}), 404
    return jsonify(order)
