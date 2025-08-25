from app import db

# B. G. L. 25/08/2025 Crear modelo para conectarse a la tabla OrderStatusHistory
class OrderStatusHistory(db.Model):
    __tablename__ = "OrderStatusHistory"

    history_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("Orders.order_id"), nullable=False)
    old_status = db.Column(db.String(50))
    new_status = db.Column(db.String(50), nullable=False)
    change_date = db.Column(db.DateTime, server_default=db.func.now())
    changed_by = db.Column(db.String(100))

    def __repr__(self):
        return f"<OrderStatusHistory Order:{self.order_id} {self.old_status} -> {self.new_status}>"
