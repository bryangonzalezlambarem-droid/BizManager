from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuración desde config.py
    app.config.from_object("app.config.Config")

    # Inicializar la base de datos
    db.init_app(app)

    # Registrar Blueprints (controladores)
    from app.controllers.customer_controller import customer_bp
    from app.controllers.product_controller import product_bp
    from app.controllers.salesperson_controller import salesperson_bp
    from app.controllers.order_controller import order_bp

    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(product_bp, url_prefix="/products")
    app.register_blueprint(salesperson_bp, url_prefix="/salespeople")
    app.register_blueprint(order_bp, url_prefix="/orders")

    return app
