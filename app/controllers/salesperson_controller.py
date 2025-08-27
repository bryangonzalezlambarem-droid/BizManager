from flask import Blueprint, request, jsonify
from app import db
from app.models.salesperson import Salesperson

# B. G. L. 25/08/2025 Crear blueprint para la tabla salesperson
salesperson_bp = Blueprint("salesperson_bp", __name__)

# B. G. L. 25/08/2025 Crear vendedor
@salesperson_bp.route("/salespersons", methods=["POST"])
def create_salesperson():
    data = request.get_json()
    new_salesperson = Salesperson(
        name=data["name"],
        email=data["email"],
        phone=data["phone"]
    )
    db.session.add(new_salesperson)
    db.session.commit()
    return jsonify({"message": "Vendedor creado exitosamente"}), 201

# B. G. L. 25/08/2025 Obtener todos los vendedores
@salesperson_bp.route("/salespersons", methods=["GET"])
def get_salespersons():
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
    ])

# B. G. L. 25/08/2025 Obtener un vendedor por ID
@salesperson_bp.route("/salespersons/<int:id>", methods=["GET"])
def get_salesperson(salesman_id):
    salesperson = Salesperson.query.get_or_404(salesman_id)
    return jsonify({
        "salesman_id": salesperson.salesman_id,
        "name": salesperson.name,
        "email": salesperson.email,
        "phone": salesperson.phone,
        "registration_date": salesperson.registration_date.isoformat() if salesperson.registration_date else None
    })

# B. G. L. 25/08/2025 Actualizar vendedor
@salesperson_bp.route("/salespersons/<int:id>", methods=["PUT"])
def update_salesperson(salesman_id):
    salesperson = Salesperson.query.get_or_404(salesman_id)
    data = request.get_json()
    salesperson.name = data.get("name", salesperson.name)
    salesperson.email = data.get("email", salesperson.email)
    salesperson.phone = data.get("phone", salesperson.phone)
    db.session.commit()
    return jsonify({"message": "Vendedor actualizado correctamente"})

# B. G. L. 25/08/2025 Eliminar vendedor
@salesperson_bp.route("/salespersons/<int:id>", methods=["DELETE"])
def delete_salesperson(salesman_id):
    salesperson = Salesperson.query.get_or_404(salesman_id)
    db.session.delete(salesperson)
    db.session.commit()
    return jsonify({"message": "Vendedor eliminado"})
