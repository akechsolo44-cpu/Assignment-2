from flask import Flask, render_template, session, redirect, url_for, request, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "campuswear-secret-key"


# =========================
# DATABASE FUNCTIONS
# =========================

def get_products():
    conn = sqlite3.connect("campuswear.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    conn.close()

    return products


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():

    products = get_products()

    return render_template(
        "home.html",
        products=products
    )


# =========================
# PRODUCTS PAGE
# =========================

@app.route("/products")
def products():

    search = request.args.get("search", "")
    category = request.args.get("category", "")

    conn = sqlite3.connect("campuswear.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    query = "SELECT * FROM products WHERE 1=1"
    values = []

    if search:
        query += " AND name LIKE ?"
        values.append("%" + search + "%")

    if category:
        query += " AND category = ?"
        values.append(category)

    cursor.execute(query, values)

    products = cursor.fetchall()

    conn.close()

    return render_template(
        "products.html",
        products=products,
        search=search,
        category=category
    )


# =========================
# PRODUCT DETAILS
# =========================

@app.route("/product/<int:id>")
def product_detail(id):

    products = get_products()

    selected_product = None

    for product in products:
        if product["id"] == id:
            selected_product = product
            break

    return render_template(
        "product_detail.html",
        product=selected_product
    )


# =========================
# ADD TO CART
# =========================

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):

    conn = sqlite3.connect("campuswear.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE id=?",
        (product_id,)
    )

    product = cursor.fetchone()

    conn.close()

    if product["stock"] <= 0:
        return redirect(url_for("products"))

    cart = session.get("cart", [])

    cart.append(product_id)

    session["cart"] = cart

    flash("Product added to cart successfully!", "success")

    return redirect(url_for("cart"))


# =========================
# REMOVE FROM CART
# =========================

@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):

    cart = session.get("cart", [])

    while product_id in cart:

        cart.remove(product_id)

    session["cart"] = cart

    next_page = request.args.get("next")

    if next_page == "review":

        return redirect(url_for("order_review"))

    return redirect(url_for("cart"))


# =========================
# CLEAR CART
# =========================

@app.route("/clear_cart")
def clear_cart():

    session["cart"] = []

    return redirect(url_for("cart"))


# =========================
# CART PAGE
# =========================

@app.route("/cart")
def cart():

    cart_ids = session.get("cart", [])

    products = get_products()

    cart_items = []
    total = 0

    for product in products:

        if product["id"] in cart_ids:

            cart_items.append(product)

            total += product["price"]

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("campuswear.db")
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO users
                (username, email, password, role)
                VALUES (?, ?, ?, ?)
                """,
                (
                    username,
                    email,
                    password,
                    "customer"
                )
            )

            conn.commit()

        except sqlite3.IntegrityError:

            conn.close()

            return "Email already registered!"

        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("campuswear.db")
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM users
            WHERE username=? AND password=?
            """,
            (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session["user"] = user["username"]
            session["role"] = user["role"]

            if user["role"] == "admin":

                return redirect(url_for("admin"))

            return redirect(url_for("home"))

        return "Invalid username or password"

    return render_template("login.html")


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(url_for("home"))


# =========================
# ABOUT
# =========================

@app.route("/about")
def about():
    return render_template("about.html")


# =========================
# CONTACT
# =========================

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        flash(
            "Thank you! Your message has been received. We'll get back to you soon.",
            "success"
        )

        return redirect(url_for("contact"))

    return render_template("contact.html")


# =========================
# TEST DATABASE
# =========================

@app.route("/test")
def test():

    products = get_products()

    for product in products:
        print(dict(product))

    return "Check terminal"


# =========================
# RUN APP
# =========================

@app.route("/checkout")
def checkout():

    if "user" not in session:
        return redirect(url_for("login"))

    cart_ids = session.get("cart", [])

    products = get_products()

    total = 0

    for product in products:

        if product["id"] in cart_ids:

            total += product["price"]

    return render_template(
        "payment.html",
        total=total
    )

@app.route("/order_success")
def order_success():

    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("campuswear.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, total, order_date
        FROM orders
        WHERE username = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (session["user"],)
    )

    order = cursor.fetchone()

    conn.close()

    total = 0
    order_date = ""

    if order:
        total = order["total"]
        order_date = order["order_date"]

        order_number = f"CW-{1000 + order['id']}"

    return render_template(
        "order_success.html",
        total=total,
        order_number=order_number,
        order_date=order_date
    )

@app.route("/place_order")
def place_order():

    if "user" not in session:
        return redirect(url_for("login"))

    cart_ids = session.get("cart", [])

    products = get_products()

    total = 0

    for product in products:

        if product["id"] in cart_ids:
            total += product["price"]

    conn = sqlite3.connect("campuswear.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO orders (username, total)
        VALUES (?, ?)
        """,
        (session["user"], total)
    )

    conn.commit()
    conn.close()

    session["cart"] = []

    return redirect(url_for("order_success"))

@app.route("/my_orders")
def my_orders():

    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("campuswear.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM orders
        WHERE username = ?
        ORDER BY id DESC
        """,
        (session["user"],)
    )

    orders = cursor.fetchall()

    conn.close()

    return render_template(
        "my_orders.html",
        orders=orders
    )

@app.route("/admin")
def admin():

    if "user" not in session or session.get("role") != "admin":

        return redirect(url_for("login"))

    conn = sqlite3.connect("campuswear.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(total) FROM orders")
    total_revenue = cursor.fetchone()[0]

    conn.close()

    if total_revenue is None:
        total_revenue = 0

    return render_template(
        "admin.html",
        products=products,
        total_orders=total_orders,
        total_revenue=total_revenue
    )

@app.route("/delete_product/<int:id>")
def delete_product(id):

    if "user" not in session or session.get("role") != "admin":

        return redirect(url_for("login"))

    conn = sqlite3.connect("campuswear.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM products
        WHERE id=?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("admin"))

@app.route("/add_product", methods=["GET", "POST"])
def add_product():

    if "user" not in session or session.get("role") != "admin":

        return redirect(url_for("login"))

    if request.method == "POST":

        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]
        image = request.form["image"]
        stock = request.form["stock"]

        conn = sqlite3.connect("campuswear.db")

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO products
            (name, price, description, image, stock)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                (
                name,
                price,
                description,
                image,
                stock
                )
            )
        )

        conn.commit()
        conn.close()

        return redirect(url_for("admin"))

    return render_template("add_product.html")

@app.route("/edit_product/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    if "user" not in session or session.get("role") != "admin":

        return redirect(url_for("login"))

    conn = sqlite3.connect("campuswear.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]
        image = request.form["image"]
        stock = request.form["stock"]

        cursor.execute(
            """
            UPDATE products
            SET
                name=?,
                price=?,
                description=?,
                image=?,
                stock=?
            WHERE id=?
            """,
            (
                (
                    name,
                    price,
                    description,
                    image,
                    stock,
                    id
                )
            )
        )

        conn.commit()
        conn.close()

        return redirect(url_for("admin"))

    cursor.execute(
        """
        SELECT * FROM products
        WHERE id=?
        """,
        (id,)
    )

    product = cursor.fetchone()

    conn.close()

    return render_template(
        "edit_product.html",
        product=product
    )

@app.route("/admin_orders")
def admin_orders():

    if "user" not in session or session.get("role") != "admin":

        return redirect(url_for("login"))

    conn = sqlite3.connect("campuswear.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM orders
        ORDER BY id DESC
    """)

    orders = cursor.fetchall()

    conn.close()

    return render_template(
        "admin_orders.html",
        orders=orders
    )

@app.route("/sales_dashboard")
def sales_dashboard():

    if "user" not in session or session.get("role") != "admin":

        return redirect(url_for("login"))

    conn = sqlite3.connect("campuswear.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(total) FROM orders")
    total_revenue = cursor.fetchone()[0]

    if total_revenue is None:
        total_revenue = 0

    cursor.execute("""
        SELECT *
        FROM orders
        ORDER BY id DESC
    """)

    orders = cursor.fetchall()

    conn.close()

    return render_template(
        "sales_dashboard.html",
        total_orders=total_orders,
        total_revenue=total_revenue,
        orders=orders
    )

@app.route("/payment", methods=["POST"])
def payment():

    if "user" not in session:
        return redirect(url_for("login"))

    payment_method = request.form["payment"]
    card_name = request.form["card_name"]
    card_number = request.form["card_number"]
    expiry = request.form["expiry"]
    cvv = request.form["cvv"]

    # Basic Validation

    if len(card_number) != 16:

        flash("Card number must contain exactly 16 digits.", "error")

        return redirect(url_for("checkout"))

    if len(cvv) not in [3, 4]:

        flash("Invalid CVV.", "error")

        return redirect(url_for("checkout"))

    cart_ids = session.get("cart", [])

    products = get_products()

    total = 0

    conn = sqlite3.connect("campuswear.db")
    cursor = conn.cursor()

    for product in products:

        if product["id"] in cart_ids:

            total += product["price"]

            cursor.execute(
                """
                UPDATE products
                SET stock = stock - 1
                WHERE id = ?
                """,
                (product["id"],)
            )

    cursor.execute(
        """
        INSERT INTO orders (username, total)
        VALUES (?, ?)
        """,
        (
            session["user"],
            total
        )
    )

    conn.commit()
    conn.close()

    session["cart"] = []

    flash(
        f"Payment successful using {payment_method}!",
        "success"
    )

    return redirect(url_for("processing_payment"))

@app.route("/processing_payment")
def processing_payment():

    return render_template("processing_payment.html")

@app.route("/email_confirmation")
def email_confirmation():

    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("campuswear.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, total
        FROM orders
        WHERE username = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (session["user"],)
    )

    order = cursor.fetchone()

    conn.close()

    total = 0
    order_number = ""

    if order:

        total = order["total"]
        order_number = f"CW-{1000 + order['id']}"

    return render_template(
        "email_confirmation.html",
        total=total,
        order_number=order_number
    )

@app.route("/order_review")
def order_review():

    if "user" not in session:
        return redirect(url_for("login"))

    cart_ids = session.get("cart", [])

    products = get_products()

    order_items = []

    total = 0

    for product in products:

        quantity = cart_ids.count(product["id"])

        if quantity > 0:

            item = dict(product)

            item["quantity"] = quantity

            item["subtotal"] = product["price"] * quantity

            order_items.append(item)

            total += item["subtotal"]

    return render_template(
        "order_review.html",
        order_items=order_items,
        total=total
    )

@app.route("/increase_quantity/<int:product_id>")
def increase_quantity(product_id):

    if "user" not in session:
        return redirect(url_for("login"))

    cart = session.get("cart", [])

    conn = sqlite3.connect("campuswear.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        "SELECT stock FROM products WHERE id=?",
        (product_id,)
    )

    product = cursor.fetchone()

    conn.close()

    if cart.count(product_id) < product["stock"]:

        cart.append(product_id)

        session["cart"] = cart

    return redirect(url_for("order_review"))

@app.route("/decrease_quantity/<int:product_id>")
def decrease_quantity(product_id):

    if "user" not in session:
        return redirect(url_for("login"))

    cart = session.get("cart", [])

    if product_id in cart:

        cart.remove(product_id)

        session["cart"] = cart

    return redirect(url_for("order_review"))

if __name__ == "__main__":
    app.run(debug=True)