from flask import Flask, render_template, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from dotenv import load_dotenv
from functools import wraps
from flask import request, jsonify
from app.utils.jwt_utils import decode_token

db = SQLAlchemy()

# B. G. L. 04/09/2025 
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1) B. G. L. 04/09/2025 Intentar Authorization: Bearer <token>
        auth_header = request.headers.get("Authorization", "")
        token = None
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1].strip()
        # 2) B. G. L. 04/09/2025 Si no hay header, intentar cookie
        if not token:
            token = request.cookies.get("access_token")

        payload = decode_token(token) if token else None
        if not payload:
            # B. G. L. 04/09/2025 Si el cliente quiere HTML, redigir al login. Si quiere JSON, devolver 401.
            wants_html = request.accept_mimetypes.accept_html and not request.accept_mimetypes.accept_json
            if wants_html or request.method == "GET":
                return redirect(url_for("auth.login_page"))
            return jsonify({"error": "Token inválido o expirado"}), 401

        # B. G. L. 04/09/2025 Adjuntar user al request
        request.user = payload
        return f(*args, **kwargs)
    return decorated_function

# B. G. L. 04/09/2025 Crear la app
def create_app():
    # B. G. L. 04/09/2025 Cargar variables de entorno
    load_dotenv()
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
    @jwt_required
    def index():
        products = Product.query.all()
        customers = Customer.query.all()
        salespeople = Salesperson.query.all()

        products_list = [
            {"product_id": p.product_id, "name": p.name, "price": float(p.price), "stock": p.stock}
            for p in products
        ]

        return render_template("orders.html", products=products_list, customers=customers, salespeople=salespeople, user=request.user)

    @app.route("/customers")
    @jwt_required
    def customers_page():
        customers = Customer.query.all()
        return render_template("customers.html", customers=customers, user=request.user)
    
    @app.route("/products")
    @jwt_required
    def products_page():
        products = Product.query.all()
        return render_template("products.html", products=products, user=request.user)
    
    @app.route("/salespeople")
    @jwt_required
    def salespeople_page():
        salespeople = Salesperson.query.all()
        return render_template("salespeople.html", salespeople=salespeople, user=request.user)

    return app
