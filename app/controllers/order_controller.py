from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.models.product import Product
from app.models.order_status_history import OrderStatusHistory
from datetime import datetime
from markupsafe import escape

# B. G. L. 25/08/2025 Crear blueprint para la tabla order
order_bp = Blueprint("order_bp", __name__)

# B. G. L. 29/08/2025 Lista de estados válidos
VALID_STATUSES = ["Pending", "Processing", "Shipped", "Completed", "Cancelled"]

# B. G. L. 04/09/2025 Sanitizar entradas para prevenir XSS
def sanitize_input(value):
    if isinstance(value, str):
        return escape(value.strip())
    return value

# B. G. L. 29/08/2025 Crear un nuevo pedido con detalles
@order_bp.route("/", methods=["POST"])
def create_order():
    try:
        data = request.get_json()

        if not data or "customer_id" not in data or "details" not in data:
            return jsonify({"error": "Datos incompletos: se requiere customer_id y details"}), 400

        if not isinstance(data["customer_id"], int) or data["customer_id"] <= 0:
            return jsonify({"error": "customer_id inválido"}), 400

        if not isinstance(data["details"], list) or len(data["details"]) == 0:
            return jsonify({"error": "La lista de detalles no puede estar vacía"}), 400

        new_order = Order(
            customer_id=data["customer_id"],
            order_date=data.get("order_date", datetime.utcnow()),
            status=data.get("status") if data.get("status") in VALID_STATUSES else "Pending",
            total_amount=0
        )
        db.session.add(new_order)
        db.session.flush()

        total_amount = 0
        for detail in data["details"]:
            product_id = detail.get("product_id")
            quantity = detail.get("quantity")

            if not isinstance(product_id, int) or product_id <= 0:
                return jsonify({"error": "product_id inválido"}), 400
            if not isinstance(quantity, int) or quantity <= 0:
                return jsonify({"error": f"Cantidad inválida para producto {product_id}"}), 400

            product = Product.query.get(product_id)
            if not product:
                db.session.rollback()
                return jsonify({"error": f"Producto {product_id} no encontrado"}), 404

            if product.stock < quantity:
                db.session.rollback()
                return jsonify({"error": f"Stock insuficiente para {product.name}"}), 400

            unit_price = float(product.price)
            line_total = quantity * unit_price
            total_amount += line_total

            order_detail = OrderDetail(
                order_id=new_order.order_id,
                product_id=product_id,
                salesman_id=detail.get("salesman_id"),
                quantity=quantity,
                unit_price=unit_price
            )
            db.session.add(order_detail)

            # Reducir stock
            product.stock -= quantity

        new_order.total_amount = total_amount
        db.session.commit()

        return jsonify({"message": "Pedido creado exitosamente", "order_id": new_order.order_id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno", "details": str(e)}), 500


# B. G. L. 29/08/2025 Obtener todos los pedidos (con paginación)
@order_bp.route("/", methods=["GET"])
def get_orders():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        if page < 1 or per_page < 1 or per_page > 100:
            return jsonify({"error": "Parámetros de paginación inválidos"}), 400

        pagination = Order.query.paginate(page=page, per_page=per_page, error_out=False)
        orders = pagination.items

        result = [
            {
                "order_id": o.order_id,
                "customer_id": o.customer_id,
                "order_date": o.order_date.isoformat() if o.order_date else None,
                "status": o.status,
                "total_amount": float(o.total_amount),
                "details": [
                    {
                        "detail_id": d.detail_id,
                        "product_id": d.product_id,
                        "salesman_id": d.salesman_id,
                        "quantity": d.quantity,
                        "unit_price": float(d.unit_price)
                    }
                    for d in o.order_details
                ]
            }
            for o in orders
        ]

        return jsonify({
            "orders": result,
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page
        }), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener pedidos", "details": str(e)}), 500


# B. G. L. 29/08/2025 Obtener pedido por ID
@order_bp.route("/<int:order_id>", methods=["GET"])
def get_order(order_id):
    if order_id <= 0:
        return jsonify({"error": "order_id inválido"}), 400

    try:
        order = Order.query.get_or_404(order_id)
        return jsonify({
            "order_id": order.order_id,
            "customer_id": order.customer_id,
            "order_date": order.order_date.isoformat() if order.order_date else None,
            "status": order.status,
            "total_amount": float(order.total_amount),
            "details": [
                {
                    "detail_id": d.detail_id,
                    "product_id": d.product_id,
                    "salesman_id": d.salesman_id,
                    "quantity": d.quantity,
                    "unit_price": float(d.unit_price)
                }
                for d in order.order_details
            ]
        }), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener pedido", "details": str(e)}), 500


# B. G. L. 29/08/2025 Cambiar el estado de un pedido y guardar historial
@order_bp.route("/<int:order_id>/status", methods=["PUT"])
def update_order_status(order_id):
    try:
        if order_id <= 0:
            return jsonify({"error": "order_id inválido"}), 400

        data = request.get_json()
        new_status = data.get("new_status")
        changed_by = sanitize_input(data.get("changed_by", "system"))

        if not new_status or new_status not in VALID_STATUSES:
            return jsonify({"error": "Estado inválido"}), 400

        order = Order.query.get_or_404(order_id)
        old_status = order.status

        if new_status == old_status:
            return jsonify({"error": "El estado no ha cambiado"}), 400

        order.status = new_status

        history = OrderStatusHistory(
            order_id=order.order_id,
            old_status=old_status,
            new_status=new_status,
            changed_by=changed_by
        )
        db.session.add(history)
        db.session.commit()

        return jsonify({
            "message": "Estado actualizado",
            "order_id": order.order_id,
            "old_status": old_status,
            "new_status": new_status
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error en la base de datos", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno", "details": str(e)}), 500


# B. G. L. 29/08/2025 Obtener historial de un pedido
@order_bp.route("/<int:order_id>/history", methods=["GET"])
def get_order_history(order_id):
    if order_id <= 0:
        return jsonify({"error": "order_id inválido"}), 400

    try:
        history = OrderStatusHistory.query.filter_by(order_id=order_id).all()
        return jsonify([
            {
                "history_id": h.history_id,
                "order_id": h.order_id,
                "old_status": h.old_status,
                "new_status": h.new_status,
                "change_date": h.change_date.isoformat() if h.change_date else None,
                "changed_by": h.changed_by
            }
            for h in history
        ]), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener historial", "details": str(e)}), 500


# B. G. L. 03/09/2025 Eliminar un pedido y sus detalles
@order_bp.route("/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    try:
        if order_id <= 0:
            return jsonify({"error": "order_id inválido"}), 400

        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": f"Pedido {order_id} eliminado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "No se pudo eliminar el pedido", "details": str(e)}), 500
