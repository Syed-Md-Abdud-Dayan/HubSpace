from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
from mysql.connector import Error
import requests
import uuid
import time

app = Flask(__name__)
app.secret_key = "S0m3V3ry$tr0ng@ndL0ngK3y!"

# -------------------- DATABASE --------------------
def get_db_connection():
    """Establish a MySQL connection with auto-reconnect."""
    while True:
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="", 
                database="hubspace",
                port=3306
            )
            return conn
        except Error as e:
            print("DB connection failed. Retrying in 2 seconds...", e)
            time.sleep(2)

# -------------------- HOME --------------------
@app.route('/')
def home():
    return render_template('index.html')

# -------------------- BOOK --------------------
@app.route('/book', methods=['GET', 'POST'])
def book_pc():
    if request.method == 'GET':
        return render_template('book.html')

    name = request.form['name']
    phone = request.form['phone']
    category = request.form['category']
    date = request.form['date']
    start_time = request.form['start_time']
    hours = int(request.form.get('hours', 1))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pcs WHERE category=%s AND is_available=1 LIMIT 1", (category,))
    pc = cursor.fetchone()
    if not pc:
        cursor.close()
        conn.close()
        return render_template('error.html', message="No available PC for this category!")

    cursor.execute("UPDATE pcs SET is_available=0 WHERE pc_number=%s", (pc['pc_number'],))
    conn.commit()

    cursor.execute(
        "INSERT INTO reservations (name, phone, category, date, start_time, pc_number, hours) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (name, phone, category, date, start_time, pc['pc_number'], hours)
    )
    conn.commit()
    reservation_id = cursor.lastrowid
    cursor.close()
    conn.close()

    amount = hours * 100
    return redirect(f"/pay_booking/{reservation_id}?amount={amount}&name={name}&phone={phone}")

# -------------------- MENU --------------------
@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/order')
def order():
    return render_template('order.html')

# -------------------- CONTACT & FAQ --------------------
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

# -------------------- ADMIN --------------------
@app.route('/admin_login', methods=['GET','POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username=="admin" and password=="admin123":
            session['admin_logged_in'] = True
            return redirect('/admin')
        else:
            error = "Invalid username or password."
    return render_template('admin_login.html', error=error)

@app.route('/admin')
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect('/admin_login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM reservations ORDER BY date, start_time")
    reservations = cursor.fetchall()
    cursor.execute("SELECT * FROM pcs ORDER BY pc_number")
    pcs = cursor.fetchall()
    cursor.execute("SELECT * FROM orders ORDER BY timestamp DESC")
    orders = cursor.fetchall()
    for order in orders:
        order['items_list'] = [i.strip() for i in order['items'].split(',')] if order['items'] else []

    cursor.close()
    conn.close()
    return render_template('admin.html', reservations=reservations, pcs=pcs, orders=orders)

@app.route('/toggle_pc', methods=['POST'])
def toggle_pc():
    if not session.get('admin_logged_in'):
        return redirect('/admin_login')

    pc_number = request.form['pc_number']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT is_available FROM pcs WHERE pc_number=%s", (pc_number,))
    row = cursor.fetchone()
    if row:
        new_status = 0 if row['is_available']==1 else 1
        cursor.execute("UPDATE pcs SET is_available=%s WHERE pc_number=%s", (new_status, pc_number))
        conn.commit()

    cursor.close()
    conn.close()
    return redirect('/admin')

@app.route('/delete_reservation', methods=['POST'])
def delete_reservation():
    if not session.get('admin_logged_in'):
        return redirect('/admin_login')
    res_id = request.form['reservation_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reservations WHERE id=%s", (res_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/admin')

@app.route('/delete_order', methods=['POST'])
def delete_order():
    if not session.get('admin_logged_in'):
        return redirect('/admin_login')
    order_id = request.form['order_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id=%s", (order_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/admin')

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect('/admin_login')

# -------------------- SUBMIT ORDER --------------------
@app.route('/submit_order', methods=['POST'])
def submit_order():
    pc_number = request.form.get('pc_number')
    items_str = request.form.get('selected_items')
    total_price = float(request.form.get('total_amount', 0))

    if not pc_number or not items_str or total_price <=0:
        return render_template('error.html', message="PC number, items, or amount missing.")

    items = [item.strip() for item in items_str.split(',') if item.strip()]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (pc_number, items, total_price) VALUES (%s,%s,%s)",
        (pc_number, ",".join(items), total_price)
    )
    conn.commit()
    order_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return redirect(f"/pay_order/{order_id}")

# -------------------- PAYMENT --------------------
def initiate_payment(amount, tran_id, name, phone, success_url, fail_url, cancel_url, product_name, category):
    url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
    payload = {
        'store_id':'hubsp68a9dff51b716',
        'store_passwd':'hubsp68a9dff51b716@ssl',
        'total_amount':amount,
        'currency':'BDT',
        'tran_id':tran_id,
        'success_url':success_url,
        'fail_url':fail_url,
        'cancel_url':cancel_url,
        'cus_name':name,
        'cus_email':'test@example.com',
        'cus_phone':phone,
        'cus_add1':'Dhaka',
        'cus_city':'Dhaka',
        'cus_country':'Bangladesh',
        'shipping_method':'NO',
        'product_name':product_name,
        'product_category':category,
        'product_profile':'general'
    }
    try:
        response = requests.post(url, data=payload)
        data = response.json()
        if 'GatewayPageURL' in data and data['GatewayPageURL']:
            return redirect(data['GatewayPageURL'])
        else:
            return f"SSLCommerz Error: {data}"
    except Exception as e:
        return f"Payment request failed: {e}"

@app.route('/pay_booking/<int:reservation_id>')
def pay_booking(reservation_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reservations WHERE id=%s",(reservation_id,))
    reservation = cursor.fetchone()
    cursor.close()
    conn.close()

    if not reservation:
        return render_template('error.html', message="Booking not found.")
    amount = float(request.args.get('amount',0))
    name = request.args.get('name',"Booking User")
    phone = request.args.get('phone',"01700000000")
    tran_id = str(uuid.uuid4())
    return initiate_payment(
        amount, tran_id, name, phone,
        f"http://127.0.0.1:5000/payment/success_booking/{reservation_id}",
        f"http://127.0.0.1:5000/payment/fail_booking/{reservation_id}",
        f"http://127.0.0.1:5000/payment/cancel_booking/{reservation_id}",
        "PC Booking","Reservation"
    )

@app.route('/pay_order/<int:order_id>')
def pay_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE id=%s",(order_id,))
    order = cursor.fetchone()
    cursor.close()
    conn.close()

    if not order:
        return render_template('error.html', message="Order not found.")
    amount = float(order['total_price'])
    name = "Food Order"
    phone = "01700000000"
    tran_id = str(uuid.uuid4())
    return initiate_payment(
        amount, tran_id, name, phone,
        f"http://127.0.0.1:5000/payment/success_order/{order_id}",
        f"http://127.0.0.1:5000/payment/fail_order/{order_id}",
        f"http://127.0.0.1:5000/payment/cancel_order/{order_id}",
        "Food Order","Food/Drinks"
    )

# -------------------- PAYMENT CALLBACKS --------------------
@app.route('/payment/success_booking/<int:reservation_id>', methods=['GET','POST'])
def payment_success_booking(reservation_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reservations WHERE id=%s",(reservation_id,))
    reservation = cursor.fetchone()
    cursor.close()
    conn.close()

    if not reservation:
        return render_template('error.html', message="Booking not found!")
    return render_template('success.html', pc_number=reservation['pc_number'])

@app.route('/payment/fail_booking/<int:reservation_id>', methods=['GET','POST'])
def payment_fail_booking(reservation_id):
    return render_template('error.html', message="Booking payment failed!")

@app.route('/payment/cancel_booking/<int:reservation_id>', methods=['GET','POST'])
def payment_cancel_booking(reservation_id):
    return render_template('error.html', message="Booking payment cancelled!")

@app.route('/payment/success_order/<int:order_id>', methods=['GET','POST'])
def payment_success_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE id=%s",(order_id,))
    order = cursor.fetchone()
    cursor.close()
    conn.close()

    if not order:
        return render_template('error.html', message="Order not found!")
    items = [i.strip() for i in order['items'].split(',') if i.strip()]
    return render_template('order_success.html', pc_number=order['pc_number'], items=items)

@app.route('/payment/fail_order/<int:order_id>', methods=['GET','POST'])
def payment_fail_order(order_id):
    return render_template('error.html', message="Order payment failed!")

@app.route('/payment/cancel_order/<int:order_id>', methods=['GET','POST'])
def payment_cancel_order(order_id):
    return render_template('error.html', message="Order payment cancelled!")

# -------------------- ERROR --------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="Page not found."),404

# -------------------- RUN --------------------
if __name__=="__main__":
    app.run(debug=True)
