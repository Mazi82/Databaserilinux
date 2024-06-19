from flask_mongoengine import MongoEngine

db = MongoEngine()

class Product(db.Document):
    name = db.StringField(required=True)
    price = db.FloatField(required=True)
    amount = db.IntField(required=True)
    created_at = db.DateTimeField(required=True)
    updated_at = db.DateTimeField(required=True)

class Customer(db.Document):
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    street = db.StringField(required=True)
    postal_code = db.StringField(required=True)
    age = db.IntField(required=True)
    created_at = db.DateTimeField(required=True)
    updated_at = db.DateTimeField(required=True)

class Staff(db.Document):
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    employee_since = db.DateTimeField(required=True)
    age = db.IntField(required=True)
    created_at = db.DateTimeField(required=True)
    updated_at = db.DateTimeField(required=True)

class Order(db.Document):
    product_id = db.ReferenceField(Product, required=True)
    customer_id = db.ReferenceField(Customer, required=True)
    staff_id = db.ReferenceField(Staff, required=True)
    created_at = db.DateTimeField(required=True)
    updated_at = db.DateTimeField(required=True)
