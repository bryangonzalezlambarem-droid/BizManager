from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models.salesperson import Salesperson
import re

# B. G. L. 27/08/2025 Crear blueprint para la tabla Salespersons
salesperson_bp = Blueprint("salesperson_bp", __name__)

EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"

# B. G. L 03/09/2025 Crear vendedor con password
@salesperson_bp.route("/", methods=["POST"])
def create_salesperson():
    try:
        data = request.get_json()
        required_fields = ["name", "email", "phone", "password"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Falta el campo {field}"}), 400

        if not re.match(EMAIL_REGEX, data["email"]):
            return jsonify({"error": "Email inválido"}), 400

        if len(data["phone"]) < 7 or len(data["phone"]) > 15:
            return jsonify({"error": "Teléfono inválido"}), 400

        # B. G. L 03/09/2025 Crear vendedor y asignar password
        new_salesperson = Salesperson(
            name=data["name"],
            email=data["email"],
            phone=data["phone"]
        )
        new_salesperson.set_password(data["password"])

        db.session.add(new_salesperson)
        db.session.commit()
        return jsonify({"message": "Vendedor creado exitosamente", "salesman_id": new_salesperson.salesman_id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno", "details": str(e)}), 500


# B. G. L 03/09/2025 Obtener todos los vendedores
@salesperson_bp.route("/", methods=["GET"])
def get_salespersons():
    try:
        salespersons = Salesperson.query.all()
        return jsonify([
            {
                "salesman_id": s.salesman_id,
                "name": s.name,
                "email": s.email,
                "phone": s.phone,
                "registration_date": s.registration_date.isoformat() if s.registration_date else None
            }
            for s in salespersons
        ]), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500


# B. G. L 03/09/2025 Obtener vendedor por ID
@salesperson_bp.route("/<int:salesman_id>", methods=["GET"])
def get_salesperson(salesman_id):
    try:
        salesperson = Salesperson.query.get_or_404(salesman_id)
        return jsonify({
            "salesman_id": salesperson.salesman_id,
            "name": salesperson.name,
            "email": salesperson.email,
            "phone": salesperson.phone,
            "registration_date": salesperson.registration_date.isoformat() if salesperson.registration_date else None
        }), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500

# B. G. L 03/09/2025 Actualizar vendedor (incluye password opcional)
@salesperson_bp.route("/<int:salesman_id>", methods=["PUT"])
def update_salesperson(salesman_id):
    try:
        salesperson = Salesperson.query.get_or_404(salesman_id)
        data = request.get_json()

        if "name" in data and data["name"]:
            salesperson.name = data["name"]

        if "email" in data and data["email"]:
            if not re.match(EMAIL_REGEX, data["email"]):
                return jsonify({"error": "Email inválido"}), 400
            salesperson.email = data["email"]

        if "phone" in data and data["phone"]:
            if len(data["phone"]) < 7 or len(data["phone"]) > 15:
                return jsonify({"error": "Teléfono inválido"}), 400
            salesperson.phone = data["phone"]

        if "password" in data and data["password"]:
            salesperson.set_password(data["password"])

        db.session.commit()
        return jsonify({"message": "Vendedor actualizado correctamente"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno", "details": str(e)}), 500

# B. G. L 03/09/2025 Eliminar vendedor
@salesperson_bp.route("/<int:salesman_id>", methods=["DELETE"])
def delete_salesperson(salesman_id):
    try:
        salesperson = Salesperson.query.get_or_404(salesman_id)
        db.session.delete(salesperson)
        db.session.commit()
        return jsonify({"message": "Vendedor eliminado"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno", "details": str(e)}), 500
