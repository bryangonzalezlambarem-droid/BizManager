from flask import Flask, render_template, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

db = SQLAlchemy()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("salesman_id"):
            return redirect(url_for("auth.login_page"))
        return f(*args, **kwargs)
    return decorated_function

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    db.init_app(app)

    # B. G. L. 03/09/2025 Registrar Blueprints
    from app.controllers.customer_controller import customer_bp
    from app.controllers.product_controller import product_bp
    from app.controllers.salesperson_controller import salesperson_bp
    from app.controllers.order_controller import order_bp
    from app.controllers.auth_controller import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(customer_bp, url_prefix="/api/customers")
    app.register_blueprint(product_bp, url_prefix="/api/products")
    app.register_blueprint(salesperson_bp, url_prefix="/api/salespersons")
    app.register_blueprint(order_bp, url_prefix="/api/orders")

    from app.models.customer import Customer
    from app.models.product import Product
    from app.models.salesperson import Salesperson

    # B. G. L. 03/09/2025 Rutas frontend protegidas con login_required
    @app.route("/")
    @login_required
    def index():
        products = Product.query.all()
        customers = Customer.query.all()
        salespeople = Salesperson.query.all()

        products_list = [
            {"product_id": p.product_id, "name": p.name, "price": float(p.price), "stock": p.stock}
            for p in products
        ]

        return render_template("orders.html", products=products_list, customers=customers, salespeople=salespeople)

    @app.route("/customers")
    @login_required
    def customers_page():
        customers = Customer.query.all()
        return render_template("customers.html", customers=customers)
    
    @app.route("/products")
    @login_required
    def products_page():
        products = Product.query.all()
        return render_template("products.html", products=products)
    
    @app.route("/salespeople")
    @login_required
    def salespeople_page():
        salespeople = Salesperson.query.all()
        return render_template("salespeople.html", salespeople=salespeople)

    return app
