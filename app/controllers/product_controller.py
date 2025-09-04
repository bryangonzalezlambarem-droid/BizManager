from flask import Blueprint, request, jsonify, session
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models.product import Product
from markupsafe import escape

# B. G. L. 25/08/2025 Crear blueprint para la tabla Product
product_bp = Blueprint("product_bp", __name__)

# B. G. L. 04/09/2025 Sanitizar entradas para prevenir XSS
def sanitize_input(value):
    if isinstance(value, str):
        return escape(value.strip())
    return value

# B. G. L. 25/08/2025 Crear producto
@product_bp.route("/", methods=["POST"])
def create_product():
    try:
        data = request.get_json()

        required_fields = ["name", "description", "price", "stock"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Falta el campo {field}"}), 400

        if not isinstance(data["price"], (int, float)) or data["price"] < 0:
            return jsonify({"error": "El precio debe ser un número positivo"}), 400

        if not isinstance(data["stock"], int) or data["stock"] < 0:
            return jsonify({"error": "El stock debe ser un número entero positivo"}), 400

        # Obtener salesman_id desde sesión
        salesman_id = session.get("salesman_id")
        if not salesman_id or not isinstance(salesman_id, int):
            return jsonify({"error": "Debes iniciar sesión para crear un producto"}), 401

        new_product = Product(
            name=sanitize_input(data["name"]),
            description=sanitize_input(data["description"]),
            price=float(data["price"]),
            stock=int(data["stock"]),
            salesman_id=salesman_id
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Producto creado exitosamente", "product_id": new_product.product_id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno", "details": str(e)}), 500


# B. G. L. 25/08/2025 Obtener todos los productos
@product_bp.route("/", methods=["GET"])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([
            {
                "product_id": p.product_id,
                "name": p.name,
                "description": p.description,
                "price": float(p.price),
                "stock": p.stock,
                "salesman_id": p.salesman_id
            } for p in products
        ]), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500


# B. G. L. 25/08/2025 Obtener producto por ID
@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    try:
        if product_id <= 0:
            return jsonify({"error": "ID inválido"}), 400

        product = Product.query.get_or_404(product_id)
        return jsonify({
            "product_id": product.product_id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "stock": product.stock,
            "salesman_id": product.salesman_id
        }), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500


# B. G. L. 25/08/2025 Actualizar producto
@product_bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    try:
        if product_id <= 0:
            return jsonify({"error": "ID inválido"}), 400

        product = Product.query.get_or_404(product_id)
        data = request.get_json()

        if "name" in data:
            product.name = sanitize_input(data["name"])

        if "description" in data:
            product.description = sanitize_input(data["description"])

        if "price" in data:
            try:
                price = float(data["price"])
                if price < 0:
                    return jsonify({"error": "El precio debe ser un número positivo"}), 400
                product.price = price
            except (ValueError, TypeError):
                return jsonify({"error": "El precio debe ser numérico"}), 400

        if "stock" in data:
            try:
                stock = int(data["stock"])
                if stock < 0:
                    return jsonify({"error": "El stock debe ser un número entero positivo"}), 400
                product.stock = stock
            except (ValueError, TypeError):
                return jsonify({"error": "El stock debe ser un número entero"}), 400

        if "salesman_id" in data:
            if not isinstance(data["salesman_id"], int) or data["salesman_id"] <= 0:
                return jsonify({"error": "salesman_id inválido"}), 400
            product.salesman_id = data["salesman_id"]

        db.session.commit()
        return jsonify({"message": "Producto actualizado correctamente"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno", "details": str(e)}), 500


# B. G. L. 25/08/2025 Eliminar producto
@product_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    try:
        if product_id <= 0:
            return jsonify({"error": "ID inválido"}), 400

        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Producto eliminado"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno", "details": str(e)}), 500
