from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from app.models.salesperson import Salesperson

auth_bp = Blueprint("auth", __name__)

# B. G. L 03/09/2025 Mostrar formulario login
@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

# B. G. L 03/09/2025 Procesar login (recibe JSON desde JS)
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    salesperson = Salesperson.query.filter_by(email=email).first()
    if not salesperson or not salesperson.check_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    # B. G. L 03/09/2025 Guardar vendedor logueado en sesion
    session["salesman_id"] = salesperson.salesman_id
    session["salesman_name"] = salesperson.name
    return jsonify({"message": "Login exitoso", "salesman_id": salesperson.salesman_id}), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logout exitoso"}), 200

@auth_bp.route("/me", methods=["GET"])
def me():
    if "salesman_id" not in session:
        return jsonify({"error": "No autenticado"}), 401
    return jsonify({
        "salesman_id": session["salesman_id"],
        "name": session["salesman_name"]
    })
