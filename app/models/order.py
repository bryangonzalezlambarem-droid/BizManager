from app import db

# B. G. L. 22/08/2025 Crear modelo para conectarse a la tabla Order
class Order(db.Model):
    __tablename__ = 'Orders'

    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.customer_id'), nullable=False)
    order_date = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.String(50), default='Pending')
    total_amount = db.Column(db.Numeric(10, 2), default=0)

    # B. G. L. 22/08/2025 Relacion con detalles de pedido
    order_details = db.relationship('OrderDetail', backref='order', lazy=True)
    # B. G. L. 22/08/2025 Relacion con historial de estados
    status_history = db.relationship('OrderStatusHistory', backref='order', lazy=True)

    def __repr__(self):
        return f"<Order {self.order_id} - {self.status}>"
