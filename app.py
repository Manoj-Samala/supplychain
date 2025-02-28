# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    order_date = db.Column(db.String(20))
    status = db.Column(db.String(20))

class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    shipment_date = db.Column(db.String(20))
    status = db.Column(db.String(20))

with app.app_context():
    db.create_all()

# Customer Routes
@app.route('/customers')
def customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    new_customer = Customer(
        name=request.form['name'],
        email=request.form['email'],
        phone=request.form['phone'],
        address=request.form['address']
    )
    db.session.add(new_customer)
    db.session.commit()
    return redirect(url_for('customers'))

# Order Routes
@app.route('/orders')
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

@app.route('/add_order', methods=['POST'])
def add_order():
    new_order = Order(
        customer_id=request.form['customer_id'],
        product_id=request.form['product_id'],
        quantity=request.form['quantity'],
        order_date=request.form['order_date'],
        status=request.form['status']
    )
    db.session.add(new_order)
    db.session.commit()
    return redirect(url_for('orders'))

# Shipment Routes
@app.route('/shipments')
def shipments():
    shipments = Shipment.query.all()
    return render_template('shipments.html', shipments=shipments)


@app.route('/')
def home():
    return redirect(url_for('customers'))  # Redirect to customers page by default

@app.route('/add_shipment', methods=['POST'])
def add_shipment():
    new_shipment = Shipment(
        order_id=request.form['order_id'],
        shipment_date=request.form['shipment_date'],
        status=request.form['status']
    )
    db.session.add(new_shipment)
    db.session.commit()
    return redirect(url_for('shipments'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)