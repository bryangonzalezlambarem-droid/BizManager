from app import db

# B. G. L. 22/08/2025 Crear modelo para conectarse a la tabla Customers
class Customer(db.Model):
    __tablename__ = 'Customers'
    
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    
    # B. G. L. 22/08/2025 Relacion con Orders
    orders = db.relationship('Order', backref='customer', lazy=True)
    
    def __repr__(self):
        return f"<Customer {self.name}>"
    