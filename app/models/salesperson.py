from app import db

# B. G. L. 22/08/2025 Crear modelo para conectarse a la tabla Salesperson
class Salesperson(db.Model):
    __tablename__ = 'Salespeople'
    
    salesman_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(100))
    registration_date = db.Column(db.DateTime, server_default=db.func.now())
    
    # B. G. L. 22/08/2025 Relacion con Productos
    products = db.relationship('Product', backref='salesperson', lazy=True)
    # B. G. L. 22/08/2025 Relacion con OrderDetails
    order_details = db.relationship('OrderDetail', backref='salesperson', lazy=True)
    
    def __repr__(self):
        return f"<Salesperson {self.name}>"
    
    