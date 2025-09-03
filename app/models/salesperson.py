from werkzeug.security import generate_password_hash, check_password_hash
from app import db

# B. G. L. 22/08/2025 Crear modelo para conectarse a la tabla Salesperson
class Salesperson(db.Model):
    __tablename__ = 'Salespeople'
    
    salesman_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(100))
    registration_date = db.Column(db.DateTime, server_default=db.func.now())
    password_hash = db.Column(db.String(255), nullable=False)
    
    #  B. G. L. 22/08/2025 Relacion con Productos (borrado en cascada)
    products = db.relationship(
        'Product',
        backref='salesperson',
        lazy=True,
        cascade="all, delete-orphan"
    )
    
    #  B. G. L. 22/08/2025 Relacion con OrderDetails (borrado en cascada)
    order_details = db.relationship(
        'OrderDetail',
        backref='salesperson',
        lazy=True,
        cascade="all, delete-orphan"
    )
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<Salesperson {self.name}>"
