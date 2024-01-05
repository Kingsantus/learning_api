from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
# initialize flask
app = Flask(__name__)
# create directory location
basedir = os.path.abspath(os.path.dirname(__file__))
# database creation
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'b9a17240484e9064bc6e2c6e'
# initializing db
db = SQLAlchemy(app)
# initializing marshmallow
ma = Marshmallow(app)

# product class/model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    desc = db.Column(db.String(500))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, desc, price, qty):
        self.name = name
        self.desc = desc
        self.price = price
        self.qty = qty

# product Schema field we want to show
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'desc', 'price', 'qty')

# Init schema 
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# creating a product
@app.route('/product', methods=['POST'])
def creating_product():
    name = request.json['name']
    desc = request.json['desc']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, desc, price, qty)
    db.session.add(new_product)
    db.session.commit()

    return products_schema.jsonify(new_product), 201


# fetching all product
@app.route('/product', methods=['GET'])
def get_all_product():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


# fetching single product
@app.route('/product/<id>', methods=['GET'])
def get_single_product(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    return product_schema.jsonify(product)


# updating a product
@app.route('/product/<id>', methods=['PUT'])
def updating_product(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    name = request.json['name']
    desc = request.json['desc']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.desc = desc
    product.price = price
    product.qty = qty

    db.session.commit()

    return product_schema.jsonify(product), 201

# deleting a product
# fetching single product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)
