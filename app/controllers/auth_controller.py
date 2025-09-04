from flask import Blueprint, request, jsonify, render_template, make_response
from app.models.salesperson import Salesperson
from app.utils.jwt_utils import generate_token

auth_bp = Blueprint("auth", __name__)

# B. G. L 03/09/2025 Mostrar formulario login
@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

# B. G. L 03/09/2025 Procesar login 
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    salesperson = Salesperson.query.filter_by(email=email).first()
    if not salesperson or not salesperson.check_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    token = generate_token(salesperson.salesman_id, salesperson.name)

    # B. G. L. 04/09/2025 responder JSON y setear cookie HttpOnly con el token
    resp = make_response(jsonify({"message": "Login exitoso"}), 200)
    # B. G. L. 04/09/2025 Nota: en desarrollo sin HTTPS puedes poner secure=False
    resp.set_cookie(
        "access_token",
        token,
        httponly=True,
        secure=False,      # B. G. L. 04/09/2025 cambiar a True en produccion con HTTPS
        samesite="Lax",
        max_age=3600       # B. G. L. 04/09/2025 1 hora
    )
    return resp

# B. G. L. 04/09/2025 Cerrar sesion
@auth_bp.route("/logout", methods=["POST"])
def logout():
    resp = make_response(jsonify({"message": "Logout exitoso"}), 200)
    resp.delete_cookie("access_token")
    return resp

@auth_bp.route("/me", methods=["GET"])
def me():
    # # B. G. L. 04/09/2025 Aqui puedo leer desde cookie o usar el decorador en otra ruta
    return jsonify({"message": "OK"}), 200
