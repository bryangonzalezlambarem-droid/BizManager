from flask import Blueprint, request, jsonify, render_template, make_response
from app.models.salesperson import Salesperson
from app.utils.jwt_utils import generate_token
from sqlalchemy.exc import SQLAlchemyError

auth_bp = Blueprint("auth", __name__)

# B. G. L 03/09/2025 Mostrar formulario login
@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

# B. G. L 03/09/2025 Procesar login 
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Datos de solicitud inválidos"}), 400
        
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()

        # B. G. L 03/09/2025 Validaciones basicas
        if not email or not password:
            return jsonify({"error": "Email y contraseña son requeridos"}), 400

        # B. G. L 03/09/2025 Buscar usuario
        salesperson = Salesperson.query.filter_by(email=email).first()
        
        if not salesperson:
            return jsonify({"error": "Credenciales inválidas"}), 401
        
        if not salesperson.check_password(password):
            return jsonify({"error": "Credenciales inválidas"}), 401

        # B. G. L 03/09/2025 Generar token
        token = generate_token(salesperson.salesman_id, salesperson.name)

        # B. G. L 03/09/2025 Respuesta exitosa
        resp_data = {
            "message": "Login exitoso",
            "token": token,
            "user": {
                "id": salesperson.salesman_id,
                "name": salesperson.name,
                "email": salesperson.email
            }
        }

        resp = make_response(jsonify(resp_data), 200)
        resp.set_cookie(
            "access_token",
            token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=3600
        )
        return resp

    except SQLAlchemyError:
        return jsonify({"error": "Error en la base de datos"}), 500
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500

@auth_bp.route("/logout", methods=["POST"])
def logout():
    resp = make_response(jsonify({"message": "Sesión cerrada exitosamente"}), 200)
    resp.delete_cookie("access_token")
    return resp

@auth_bp.route("/me", methods=["GET"])
def me():
    # B. G. L 03/09/2025 Implementar logica para obtener datos del usuario actual
    return jsonify({"message": "Endpoint para información del usuario"}), 200