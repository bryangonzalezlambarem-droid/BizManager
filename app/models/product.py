from app import db

# B. G. L. 22/08/2025 Crear modelo para conectarse a la tabla Product
class Product(db.Model):
    __tablename__ = 'Products'
    
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    
    # B. G. L. 22/08/2025 Clave foranea a Salespeople
    salesman_id = db.Column(db.Integer, db.ForeignKey('Salespeople.salesman_id'), nullable=False)
    # B. G. L. 22/08/2025 Relacion con OrderDetail
    order_details = db.relationship('OrderDetail', backref='product', lazy=True)
    
    def __repr__(self):
        return f"<Product {self.name}>"
    
