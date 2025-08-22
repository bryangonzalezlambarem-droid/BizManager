from app import db

# B. G. L. 22/08/2025 Crear modelo para conectarse a la tabla OrderDetails
class OrderDetail(db.Model):
    __tablename__ = 'OrderDetails'

    detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.product_id'), nullable=False)
    salesman_id = db.Column(db.Integer, db.ForeignKey('Salespeople.salesman_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f"<OrderDetail Order:{self.order_id} Product:{self.product_id}>"
