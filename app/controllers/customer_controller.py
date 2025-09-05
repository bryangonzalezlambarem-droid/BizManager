from flask import Blueprint, request, jsonify
from app import db, jwt_required
from app.models.customer import Customer
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import re
from datetime import datetime
from markupsafe import escape

# B. G. L. 25/08/2025 Crear blueprint para la tabla customer
customer_bp = Blueprint("customer_bp", __name__)

# B. G. L. 04/09/2025 Sanitizar los elementos que pasa en fronted
def sanitize_input(value):
    if isinstance(value, str):
        return escape(value.strip())
    return value

# B. G. L. 25/08/2025 Validar email
def is_valid_email(email):
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# B. G. L. 25/08/2025 Validar telefono
def is_valid_phone(phone):
    if not phone:
        return False
    pattern = r'^\+?[1-9]\d{1,14}$'
    return re.match(pattern, phone) is not None


# B. G. L. 25/08/2025 Crear cliente (requiere autenticación)
@customer_bp.route("/", methods=["POST"])
@jwt_required
def create_customer():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400

        required_fields = ["name", "email"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"El campo '{field}' es obligatorio"}), 400

        if not is_valid_email(data["email"]):
            return jsonify({"error": "El formato del email no es válido"}), 400

        if "phone" in data and data["phone"] and not is_valid_phone(data["phone"]):
            return jsonify({"error": "El formato del teléfono no es válido"}), 400

        existing_customer = Customer.query.filter_by(email=data["email"]).first()
        if existing_customer:
            return jsonify({"error": "Ya existe un cliente con este email"}), 409

        # ✅ Obtener vendedor autenticado desde JWT
        salesman_id = request.user.get("salesman_id")

        new_customer = Customer(
            name=sanitize_input(data.get("name")),
            email=sanitize_input(data.get("email")),
            phone=sanitize_input(data.get("phone")),
            address=sanitize_input(data.get("address")),
            salesman_id=salesman_id
        )

        db.session.add(new_customer)
        db.session.commit()

        return jsonify({
            "message": "Cliente creado exitosamente",
            "id": new_customer.customer_id,
            "customer": {
                "id": new_customer.customer_id,
                "name": new_customer.name,
                "email": new_customer.email,
                "phone": new_customer.phone,
                "address": new_customer.address,
                "salesman_id": new_customer.salesman_id
            }
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Error de integridad en la base de datos", "details": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500


# B. G. L. 25/08/2025 Obtener todos los clientes (no requiere auth)
@customer_bp.route("/", methods=["GET"])
def get_customers():
    try:
        customers = Customer.query.all()
        result = [
            {
                "id": c.customer_id,
                "name": c.name,
                "email": c.email,
                "phone": c.phone,
                "address": c.address,
                "salesman_id": c.salesman_id
            }
            for c in customers
        ]
        return jsonify({"customers": result, "total": len(result)})
    except Exception as e:
        return jsonify({"error": "Error al obtener los clientes", "details": str(e)}), 500


# B. G. L. 25/08/2025 Obtener cliente por id
@customer_bp.route("/<int:id>", methods=["GET"])
def get_customer(id):
    try:
        if id <= 0:
            return jsonify({"error": "ID inválido"}), 400

        customer = Customer.query.get(id)
        if not customer:
            return jsonify({"error": "Cliente no encontrado"}), 404

        return jsonify({
            "id": customer.customer_id,
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
            "address": customer.address,
            "salesman_id": customer.salesman_id
        })
    except Exception as e:
        return jsonify({"error": "Error al obtener el cliente", "details": str(e)}), 500


# B. G. L. 25/08/2025 Actualizar cliente (requiere auth)
@customer_bp.route("/<int:id>", methods=["PUT"])
@jwt_required
def update_customer(id):
    try:
        if id <= 0:
            return jsonify({"error": "ID inválido"}), 400

        customer = Customer.query.get(id)
        if not customer:
            return jsonify({"error": "Cliente no encontrado"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400

        if "email" in data and data["email"]:
            if not is_valid_email(data["email"]):
                return jsonify({"error": "El formato del email no es válido"}), 400
            existing_customer = Customer.query.filter(
                Customer.email == data["email"],
                Customer.customer_id != id
            ).first()
            if existing_customer:
                return jsonify({"error": "Ya existe otro cliente con este email"}), 409

        if "phone" in data and data["phone"] and not is_valid_phone(data["phone"]):
            return jsonify({"error": "El formato del teléfono no es válido"}), 400

        if "name" in data:
            customer.name = sanitize_input(data["name"])
        if "email" in data:
            customer.email = sanitize_input(data["email"])
        if "phone" in data:
            customer.phone = sanitize_input(data["phone"])
        if "address" in data:
            customer.address = sanitize_input(data["address"])

        customer.updated_at = datetime.utcnow()

        # B. G. L. 05/09/2025 guardar el vendedor que modifico
        customer.salesman_id = request.user.get("salesman_id")

        db.session.commit()

        return jsonify({"message": "Cliente actualizado exitosamente"})
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Error de integridad en la base de datos", "details": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500


# B. G. L. 25/08/2025 Eliminar cliente (requiere auth)
@customer_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required
def delete_customer(id):
    try:
        if id <= 0:
            return jsonify({"error": "ID inválido"}), 400

        customer = Customer.query.get(id)
        if not customer:
            return jsonify({"error": "Cliente no encontrado"}), 404

        # B. G. L. 05/09/2025 validar que el vendedor autenticado sea el creador
        salesman_id = request.user.get("salesman_id")
        if customer.salesman_id and customer.salesman_id != salesman_id:
            return jsonify({"error": "No tienes permiso para eliminar este cliente"}), 403

        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": "Cliente eliminado exitosamente"})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500
