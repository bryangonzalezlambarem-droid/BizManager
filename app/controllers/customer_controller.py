from flask import Blueprint, request, jsonify
from app import db
from app.models.customer import Customer

# B. G. L. 25/08/2025 Crear blueprint para la tabla customer
customer_bp = Blueprint("customer_bp", __name__)

# B. G. L. 25/08/2025 Crear un cliente nuevo
@customer_bp.route("/", methods=["POST"])
def create_customer():
    data = request.get_json()
    new_customer = Customer(
        name=data.get("name"),
        email=data.get("email"),
        phone=data.get("phone"),
        adress=data.get("adress")
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "Cliente creado", "id": new_customer.id}), 201

# B. G. L. 25/08/2025 Obtener todos los clientes
@customer_bp.route("/", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    result = [
        {"id": c.id, "name": c.name, "email": c.email, "phone": c.phone, "adress": c.adress}
        for c in customers
    ]
    return jsonify(result)

# B. G. L. 25/08/2025 Obtener un cliente por id
@customer_bp.route("/<int:id>", methods=["GET"])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify({"id": customer.id, "name": customer.name, "email": customer.email, "phone": customer.phone, "adress": customer.adress})

# B. G. L. 25/08/2025 Actualizar un cliente
@customer_bp.route("/<int:id>", methods=["PUT"])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json()
    customer.name = data.get("name", customer.name)
    customer.email = data.get("email", customer.email)
    customer.phone = data.get("phone", customer.phone)
    customer.adress = data.get("adress", customer.adress)
    db.session.commit()
    return jsonify({"message": "Cliente actualizado"})

# B. G. L. 25/08/2025 Actualizar un cliente
@customer_bp.route("/<int:id>", methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Cliente eliminado"})