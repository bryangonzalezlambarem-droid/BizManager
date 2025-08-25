from flask import Blueprint, request, jsonify
from app import db
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.models.product import Product
from app.models.order_status_history import OrderStatusHistory

# B. G. L. 25/08/2025 Crear blueprint para la tabla Orders
order_bp = Blueprint("order_bp", __name__)

# B. G. L. 25/08/2025 Crear un nuevo pedido con detalles
@order_bp.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    new_order = Order(
        customer_id=data["customer_id"],
        order_date=data.get("order_date"),
        status=data.get("status", "Pending"),
        total_amount=0
    )
    db.session.add(new_order)
    db.session.flush()  # B. G. L. 25/08/2025 para obtener el ID del pedido antes del commit

    total_amount = 0
    # B. G. L. 25/08/2025 Insertar detalles
    for detail in data["details"]:
        product = Product.query.get(detail["product_id"])
        if not product:
            return jsonify({"error": f"Producto {detail['product_id']} no encontrado"}), 404
        if product.stock < detail["quantity"]:
            return jsonify({"error": f"Stock insuficiente para {product.name}"}), 400

        line_total = float(detail["quantity"]) * float(detail["unit_price"])
        total_amount += line_total

        order_detail = OrderDetail(
            order_id=new_order.order_id,
            product_id=detail["product_id"],
            salesman_id=detail["salesman_id"],
            quantity=detail["quantity"],
            unit_price=detail["unit_price"]
        )
        db.session.add(order_detail)

        # B. G. L. 25/08/2025 Reducir stock del producto
        product.stock -= detail["quantity"]

    # B. G. L. 25/08/2025 Actualizar el total del pedido
    new_order.total_amount = total_amount

    db.session.commit()
    return jsonify({"message": "Pedido creado exitosamente", "order_id": new_order.order_id}), 201

# B. G. L. 25/08/2025 Obtener todos los pedidos
@order_bp.route("/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    return jsonify([
        {
            "order_id": o.order_id,
            "customer_id": o.customer_id,
            "order_date": o.order_date,
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
    ])

# B. G. L. 25/08/2025 Obtener pedido por ID
@order_bp.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({
        "order_id": order.order_id,
        "customer_id": order.customer_id,
        "order_date": order.order_date,
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
    })
    
# B. G. L. 25/08/2025 Cambiar el estado de un pedido y guardar historial
@order_bp.route("/orders/<int:order_id>/status", methods=["PUT"])
def update_order_status(order_id):
    data = request.get_json()
    new_status = data.get("new_status")
    changed_by = data.get("changed_by", "system")

    order = Order.query.get_or_404(order_id)
    old_status = order.status

    if not new_status or new_status == old_status:
        return jsonify({"error": "Estado inválido o sin cambios"}), 400

    # B. G. L. 25/08/2025 Actualizar el pedido
    order.status = new_status

    # Registrar historial
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
    })

# B. G. L. 25/08/2025 Obtener historial de un pedido
@order_bp.route("/orders/<int:order_id>/history", methods=["GET"])
def get_order_history(order_id):
    history = OrderStatusHistory.query.filter_by(order_id=order_id).all()
    return jsonify([
        {
            "history_id": h.history_id,
            "order_id": h.order_id,
            "old_status": h.old_status,
            "new_status": h.new_status,
            "change_date": h.change_date,
            "changed_by": h.changed_by
        }
        for h in history
    ])
