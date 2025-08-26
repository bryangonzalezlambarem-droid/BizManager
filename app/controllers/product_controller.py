from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product

# B. G. L. 25/08/2025 Crear blueprint para la tabla product
product_bp = Blueprint("product_bp", __name__)

# B. G. L. 25/08/2025 Crear producto
@product_bp.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    new_product = Product(
        name=data["name"],
        description=data["description"],
        price=data["price"],
        stock=data["stock"]
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Producto creado exitosamente"}), 201

# B. G. L. 25/08/2025 Obtener todos los productos 
@product_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "description": p.description, 
            "price": p.price,
            "stock": p.stock
        }
        for p in products
    ])

# B. G. L. 25/08/2025 Obtener un producto por ID
@product_bp.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,  
        "price": product.price,
        "stock": product.stock
    })

# B. G. L. 25/08/2025 Actualizar producto
@product_bp.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.stock = data.get("stock", product.stock)
    db.session.commit()
    return jsonify({"message": "Producto actualizado correctamente"})

# B. G. L. 25/08/2025 Eliminar producto
@product_bp.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Producto eliminado"})
