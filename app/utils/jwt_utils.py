import jwt
import datetime
from flask import current_app

# B. G. L. 04/09/2025 Crear json token
def generate_token(user_id, user_name):
    payload = {
        "user_id": user_id,
        "name": user_name,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # B. G. L. 04/09/2025 expira en 1h
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return token

# B. G. L. 04/09/2025 Decodificar token
def decode_token(token):
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
