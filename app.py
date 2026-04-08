from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime
import os

app = Flask(__name__)

#forming database connection 
def get_database():
    return mysql.connector.connect(
        host='DB_HOST',
        user='DB_USER',
        password='DB_PASSWORD',
        database='DB_NAME'
    )

#Home
@app.route('/')
def home():
    return render_template('index.html')

# Products:
# Show all products
@app.route('/products')
def products():
    db = get_database()
    cursor = db.cursor()  
    cursor.execute("""
        SELECT p.product_id, p.name, p.price, p.quantity, s.name
        FROM Products p
        LEFT JOIN Suppliers s ON p.supplier_id = s.supplier_id
    """)
    products = cursor.fetchall()
    cursor.execute("SELECT * FROM Suppliers")
    suppliers = cursor.fetchall()
    db.close()
    return render_template('products.html', products=products, suppliers=suppliers)

# Add a new product
@app.route('/add_product', methods=['POST'])
def add_product():
    db = get_database()
    cursor = db.cursor()
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    supplier_id = request.form['supplier_id']
    cursor.execute(
        "INSERT INTO Products (name, price, quantity, supplier_id) VALUES (%s, %s, %s, %s)",
        (name, price, quantity, supplier_id)
    )
    db.commit()
    db.close()
    return redirect(url_for('products'))

# Edit a product
@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    db = get_database()
    cursor = db.cursor()
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        supplier_id = request.form['supplier_id']
        cursor.execute(
            "UPDATE Products SET name=%s, price=%s, quantity=%s, supplier_id=%s WHERE product_id=%s",
            (name, price, quantity, supplier_id, product_id)
        )
        db.commit()
        db.close()
        return redirect(url_for('products'))
    cursor.execute("SELECT * FROM Products WHERE product_id=%s", (product_id,))
    product = cursor.fetchone()
    cursor.execute("SELECT * FROM Suppliers")
    suppliers = cursor.fetchall()
    db.close()
    return render_template('editpage.html', product=product, suppliers=suppliers)

# Delete a product
@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    db = get_database()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Products WHERE product_id=%s", (product_id,))
    db.commit()
    db.close()
    return redirect(url_for('products'))

# Suppliers:
# Show all suppliers
@app.route('/suppliers')
def suppliers():
    db = get_database()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Suppliers")
    suppliers = cursor.fetchall()
    db.close()
    return render_template('suppliers.html', suppliers=suppliers)

# Add a new supplier
@app.route('/add_supplier', methods=['POST'])
def add_supplier():
    db = get_database()
    cursor = db.cursor()
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    cursor.execute(
        "INSERT INTO Suppliers (name, phone, email) VALUES (%s, %s, %s)",
        (name, phone, email)
    )
    db.commit()
    db.close()
    return redirect(url_for('suppliers'))

# Edit a supplier
@app.route('/suppliers/edit/<int:supplier_id>', methods=['GET', 'POST'])
def edit_supplier(supplier_id):
    db = get_database()
    cursor = db.cursor()
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        cursor.execute(
            "UPDATE Suppliers SET name=%s, phone=%s, email=%s WHERE supplier_id=%s",
            (name, phone, email, supplier_id)
        )
        db.commit()
        db.close()
        return redirect(url_for('suppliers'))
    cursor.execute("SELECT * FROM Suppliers WHERE supplier_id=%s", (supplier_id,))
    supplier = cursor.fetchone()
    db.close()
    return render_template('editsupplier.html', supplier=supplier)

# Delete a supplier
@app.route('/delete_supplier/<int:supplier_id>')
def delete_supplier(supplier_id):
    db = get_database()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Suppliers WHERE supplier_id=%s", (supplier_id,))
    db.commit()
    db.close()
    return redirect(url_for('suppliers'))


# Sales:
# Show all sales
# Sales:
# Show all sales
@app.route('/sales')
def sales():
    db = get_database()
    cursor = db.cursor()
    cursor.execute("""
        SELECT s.sale_id, p.name, s.quantity, DATE(s.sale_date)
        FROM Sales s
        JOIN Products p ON s.product_id = p.product_id
    """)
    sales = cursor.fetchall()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    db.close()
    return render_template('sales.html', sales=sales, products=products)

# Add a new sale
@app.route('/add_sale', methods=['POST'])
def add_sale():
    db = get_database()
    cursor = db.cursor()
    product_id = request.form['product_id']
    quantity = request.form['quantity']
    sale_date = request.form['sale_date']
    cursor.execute("SELECT user_id FROM Users LIMIT 1")
    user = cursor.fetchone()
    if user is None:
        db.close()
        return "No users exist. Please add a user first before recording a sale.", 400
    user_id = user[0]
    cursor.execute(
        "INSERT INTO Sales (product_id, user_id, quantity, sale_date) VALUES (%s, %s, %s, %s)",
        (product_id, user_id, quantity, sale_date)
    )
    db.commit()
    db.close()
    return redirect(url_for('sales'))

# Edit a sale
@app.route('/edit_sale/<int:sale_id>', methods=['GET', 'POST'])
def edit_sale(sale_id):
    db = get_database()
    cursor = db.cursor()
    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        sale_date = request.form['sale_date']
        cursor.execute(
            "UPDATE Sales SET product_id=%s, quantity=%s, sale_date=%s WHERE sale_id=%s",
            (product_id, quantity, sale_date, sale_id)
        )
        db.commit()
        db.close()
        return redirect(url_for('sales'))
    cursor.execute("SELECT * FROM Sales WHERE sale_id=%s", (sale_id,))
    sale = cursor.fetchone()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    db.close()
    return render_template('editsale.html', sale=sale, products=products)

# Delete a sale
@app.route('/delete_sale/<int:sale_id>')
def delete_sale(sale_id):
    db = get_database()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Sales WHERE sale_id=%s", (sale_id,))
    db.commit()
    db.close()
    return redirect(url_for('sales'))

# Users:
# Show all users
@app.route('/users')
def users():
    db = get_database()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    db.close()
    return render_template('users.html', users=users)

# Add a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    db = get_database()
    cursor = db.cursor()
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']
    cursor.execute(
        "INSERT INTO Users (name, email, password, role) VALUES (%s, %s, %s, %s)",
        (name, email, password, role)
    )
    db.commit()
    db.close()
    return redirect(url_for('users'))

# Edit a user
@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    db = get_database()
    cursor = db.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        cursor.execute(
            "UPDATE Users SET name=%s, email=%s, role=%s WHERE user_id=%s",
            (name, email, role, user_id)
        )
        db.commit()
        db.close()
        return redirect(url_for('users'))
    cursor.execute("SELECT * FROM Users WHERE user_id=%s", (user_id,))
    user = cursor.fetchone()
    db.close()
    return render_template('edituser.html', user=user)

# Delete a user
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    db = get_database()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Users WHERE user_id=%s", (user_id,))
    db.commit()
    db.close()
    return redirect(url_for('users'))


# Purchase orders:
# Show all orders
@app.route('/orders')
def orders():
    db = get_database()
    cursor = db.cursor()
    cursor.execute("""
        SELECT po.purchase_id, p.name, s.name, po.quantity, po.order_date
        FROM PurchaseOrders po
        JOIN Products p ON po.product_id = p.product_id
        JOIN Suppliers s ON po.supplier_id = s.supplier_id
    """)
    orders = cursor.fetchall()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    cursor.execute("SELECT * FROM Suppliers")
    suppliers = cursor.fetchall()
    db.close()
    return render_template('orders.html', orders=orders, products=products, suppliers=suppliers)

# Add a new order
@app.route('/add_order', methods=['POST'])
def add_order():
    db = get_database()
    cursor = db.cursor()
    product_id = request.form['product_id']
    supplier_id = request.form['supplier_id']
    quantity = request.form['quantity']
    order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        "INSERT INTO PurchaseOrders (product_id, supplier_id, quantity, order_date) VALUES (%s, %s, %s, %s)",
        (product_id, supplier_id, quantity, order_date)
    )
    db.commit()
    db.close()
    return redirect(url_for('orders'))

# Delete an order
@app.route('/delete_order/<int:purchase_id>')
def delete_order(purchase_id):
    db = get_database()
    cursor = db.cursor()
    cursor.execute("DELETE FROM PurchaseOrders WHERE purchase_id=%s", (purchase_id,))
    db.commit()
    db.close()
    return redirect(url_for('orders'))

#to run the app
if __name__ == '__main__':
     port = int(os.environ.get("PORT", 5000))  # Use Railway's PORT or fallback to 5000
     app.run(host='0.0.0.0', port=port, debug=True)