from flask import Blueprint, request, jsonify
from app import db
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
        return escape(value.strip())  # B. G. L. 25/08/2025 quita espacios y escapa HTML/JS
    return value

# B. G. L. 25/08/2025 Funcion para validar email
def is_valid_email(email):
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# B. G. L. 25/08/2025 Funcion para validar telefono 
def is_valid_phone(phone):
    if not phone:
        return False
    # B. G. L. 25/08/2025 Permite numeros con formato internacional: +[código pais][numero]
    pattern = r'^\+?[1-9]\d{1,14}$'
    return re.match(pattern, phone) is not None

# B. G. L. 25/08/2025 Crear un cliente nuevo
@customer_bp.route("/", methods=["POST"])
def create_customer():
    try:
        data = request.get_json()
        
        # B. G. L. 25/08/2025 Validar que exista data
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
        
        # B. G. L. 25/08/2025 Validar campos obligatorios
        required_fields = ["name", "email"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"El campo '{field}' es obligatorio"}), 400
        
        # B. G. L. 25/08/2025 Validar formato de email
        if not is_valid_email(data["email"]):
            return jsonify({"error": "El formato del email no es válido"}), 400
        
        # B. G. L. 25/08/2025 Validar formato de telefono si se proporciona
        if "phone" in data and data["phone"] and not is_valid_phone(data["phone"]):
            return jsonify({"error": "El formato del teléfono no es válido"}), 400
        
        # B. G. L. 25/08/2025 Verificar si el email ya existe
        existing_customer = Customer.query.filter_by(email=data["email"]).first()
        if existing_customer:
            return jsonify({"error": "Ya existe un cliente con este email"}), 409
        
        new_customer = Customer(
            name=sanitize_input(data.get("name")),
            email=sanitize_input(data.get("email")),
            phone=sanitize_input(data.get("phone")),
            address=sanitize_input(data.get("address"))
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
                "address": new_customer.address
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

# B. G. L. 25/08/2025 Obtener todos los clientes
@customer_bp.route("/", methods=["GET"])
def get_customers():
    try:
        # B. G. L. 25/08/2025 Paginacion
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Validar parametros de paginacion
        if page < 1 or per_page < 1 or per_page > 100:
            return jsonify({"error": "Parámetros de paginación inválidos"}), 400
        
        customers = Customer.query.all()
        
        result = [
            {
                "id": c.customer_id,
                "name": c.name,
                "email": c.email,
                "phone": c.phone,
                "address": c.address  # coincidir con tu JS
            }
            for c in customers
        ]
        
        return jsonify({
            "customers": result,
            "total": len(result),
            "pages": 1,
            "current_page": 1
        })
        
    except Exception as e:
        return jsonify({"error": "Error al obtener los clientes", "details": str(e)}), 500

# B. G. L. 25/08/2025 Obtener un cliente por id
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
            "address": customer.address
        })
        
    except Exception as e:
        return jsonify({"error": "Error al obtener el cliente", "details": str(e)}), 500

# B. G. L. 25/08/2025 Actualizar un cliente
@customer_bp.route("/<int:id>", methods=["PUT"])
def update_customer(id):
    try:
        if id <= 0:
            return jsonify({"error": "ID inválido"}), 400
            
        customer = Customer.query.get(id)
        
        if not customer:
            return jsonify({"error": "Cliente no encontrado"}), 404
            
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400
        
        # B. G. L. 25/08/2025 Validar formato de email si se proporciona
        if "email" in data and data["email"]:
            if not is_valid_email(data["email"]):
                return jsonify({"error": "El formato del email no es válido"}), 400
                
            # B. G. L. 25/08/2025 Verificar si el email ya existe en otro cliente
            existing_customer = Customer.query.filter(
                Customer.email == data["email"], 
                Customer.customer_id != id
            ).first()
            
            if existing_customer:
                return jsonify({"error": "Ya existe otro cliente con este email"}), 409
        
        # B. G. L. 25/08/2025 Validar formato de telefono si se proporciona
        if "phone" in data and data["phone"] and not is_valid_phone(data["phone"]):
            return jsonify({"error": "El formato del teléfono no es válido"}), 400
        
        # B. G. L. 25/08/2025 Actualizar campos
        if "name" in data:
            customer.name = sanitize_input(data["name"])
        if "email" in data:
            customer.email = sanitize_input(data["email"])
        if "phone" in data:
            customer.phone = sanitize_input(data["phone"])
        if "address" in data:
            customer.address = sanitize_input(data["address"])
        
        customer.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "message": "Cliente actualizado exitosamente",
            "customer": {
                "id": customer.customer_id,
                "name": customer.name,
                "email": customer.email,
                "phone": customer.phone,
                "address": customer.address
            }
        })
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Error de integridad en la base de datos", "details": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500

# B. G. L. 25/08/2025 Eliminar un cliente
@customer_bp.route("/<int:id>", methods=["DELETE"])
def delete_customer(id):
    try:
        if id <= 0:
            return jsonify({"error": "ID inválido"}), 400
            
        customer = Customer.query.get(id)
        
        if not customer:
            return jsonify({"error": "Cliente no encontrado"}), 404
            
        db.session.delete(customer)
        db.session.commit()
        
        return jsonify({"message": "Cliente eliminado exitosamente"})
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500