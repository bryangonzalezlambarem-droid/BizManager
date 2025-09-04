from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models.salesperson import Salesperson
import re
from markupsafe import escape

# B. G. L. 27/08/2025 Crear blueprint para la tabla Salespersons
salesperson_bp = Blueprint("salesperson_bp", __name__)

EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"

# B. G. L. 04/09/2025 Sanitizar entradas para prevenir XSS
def sanitize_input(value):
    if isinstance(value, str):
        return escape(value.strip())
    return value

# B. G. L 03/09/2025 Crear vendedor con password
@salesperson_bp.route("/", methods=["POST"])
def create_salesperson():
    try:
        data = request.get_json()
        required_fields = ["name", "email", "phone", "password"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Falta el campo {field}"}), 400

        name = sanitize_input(data["name"])
        email = sanitize_input(data["email"])
        phone = sanitize_input(data["phone"])
        password = data["password"]

        if not re.match(EMAIL_REGEX, email):
            return jsonify({"error": "Email inválido"}), 400

        if len(phone) < 7 or len(phone) > 15:
            return jsonify({"error": "Teléfono inválido"}), 400

        if len(password) < 6:
            return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 400

        # Crear vendedor
        new_salesperson = Salesperson(
            name=name,
            email=email,
            phone=phone
        )
        new_salesperson.set_password(password)

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
        if salesman_id <= 0:
            return jsonify({"error": "ID inválido"}), 400

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
        if salesman_id <= 0:
            return jsonify({"error": "ID inválido"}), 400

        salesperson = Salesperson.query.get_or_404(salesman_id)
        data = request.get_json()

        if "name" in data and data["name"]:
            salesperson.name = sanitize_input(data["name"])

        if "email" in data and data["email"]:
            email = sanitize_input(data["email"])
            if not re.match(EMAIL_REGEX, email):
                return jsonify({"error": "Email inválido"}), 400
            salesperson.email = email

        if "phone" in data and data["phone"]:
            phone = sanitize_input(data["phone"])
            if len(phone) < 7 or len(phone) > 15:
                return jsonify({"error": "Teléfono inválido"}), 400
            salesperson.phone = phone

        if "password" in data and data["password"]:
            if len(data["password"]) < 6:
                return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 400
            salesperson.set_password(data["password"])

        db.session.commit()
        return jsonify({"message": "Vendedor actualizado correctamente"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno", "details": str(e)}), 500


# B. G. L 03/09/2025 Eliminar vendedor (con cascada)
@salesperson_bp.route("/<int:salesman_id>", methods=["DELETE"])
def delete_salesperson(salesman_id):
    try:
        if salesman_id <= 0:
            return jsonify({"error": "ID inválido"}), 400

        salesperson = Salesperson.query.get_or_404(salesman_id)
        db.session.delete(salesperson)
        db.session.commit()
        return jsonify({"message": "Vendedor eliminado correctamente"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno", "details": str(e)}), 500
