from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models.product import Product

#B. G. L. 25/08/2025 Crear blueprint para la tabla Product
product_bp = Blueprint("product_bp", __name__)

# B. G. L. 25/08/2025 Crear producto
@product_bp.route("/products", methods=["POST"])
def create_product():
    try:
        data = request.get_json()

        # B. G. L. 25/08/2025 Validaciones basicas
        required_fields = ["name", "description", "price", "stock"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Falta el campo {field}"}), 400

        if not isinstance(data["price"], (int, float)) or data["price"] < 0:
            return jsonify({"error": "El precio debe ser un número positivo"}), 400

        if not isinstance(data["stock"], int) or data["stock"] < 0:
            return jsonify({"error": "El stock debe ser un número entero positivo"}), 400

        new_product = Product(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            stock=data["stock"]
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Producto creado exitosamente", "id": new_product.id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno", "details": str(e)}), 500

# B. G. L. 25/08/2025 Obtener todos los productos
@product_bp.route("/products", methods=["GET"])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": p.price,
                "stock": p.stock
            } for p in products
        ]), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500

# B. G. L. 25/08/2025 Obtener producto por ID
@product_bp.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    try:
        product = Product.query.get_or_404(id)
        return jsonify({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock
        }), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500

# B. G. L. 25/08/2025 Actualizar producto
@product_bp.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    try:
        product = Product.query.get_or_404(id)
        data = request.get_json()

        if "name" in data:
            product.name = data["name"]

        if "description" in data:
            product.description = data["description"]

        if "price" in data:
            if not isinstance(data["price"], (int, float)) or data["price"] < 0:
                return jsonify({"error": "El precio debe ser un número positivo"}), 400
            product.price = data["price"]

        if "stock" in data:
            if not isinstance(data["stock"], int) or data["stock"] < 0:
                return jsonify({"error": "El stock debe ser un número entero positivo"}), 400
            product.stock = data["stock"]

        db.session.commit()
        return jsonify({"message": "Producto actualizado correctamente"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno", "details": str(e)}), 500

# B. G. L. 25/08/2025 Eliminar producto
@product_bp.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    try:
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Producto eliminado"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno", "details": str(e)}), 500
