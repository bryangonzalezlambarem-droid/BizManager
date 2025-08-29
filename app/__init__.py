from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # B. G. L. 25/08/2025 Configuracion desde config.py
    app.config.from_object("app.config.Config")

    # B. G. L. 25/08/2025 Inicializar la base de datos
    db.init_app(app)

    # B. G. L. 25/08/2025 Registrar Blueprints (API)
    from app.controllers.customer_controller import customer_bp
    from app.controllers.product_controller import product_bp
    from app.controllers.salesperson_controller import salesperson_bp
    from app.controllers.order_controller import order_bp

    app.register_blueprint(customer_bp, url_prefix="/api/customers")
    app.register_blueprint(product_bp, url_prefix="/api/products")
    app.register_blueprint(salesperson_bp, url_prefix="/api/salespersons")
    app.register_blueprint(order_bp, url_prefix="/api/orders")
    
    # B. G. L. 25/08/2025 Rutas frontend (HTML)
    from app.models.customer import Customer
    from app.models.product import Product
    from app.models.salesperson import Salesperson
    
    @app.route("/")
    def index():
        return render_template("orders.html")
    
    @app.route("/customers")
    def customers_page():
        customers = Customer.query.all()
        return render_template("customers.html", customers=customers)
    
    @app.route("/products")
    def products_page():
        products = Product.query.all()
        return render_template("products.html", products=products)
    
    @app.route("/salespeople")
    def salespeople_page():
        salespeople = Salesperson.query.all()
        return render_template("salespeople.html", salespeople=salespeople)

    return app
