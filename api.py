from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import current_user, login_user, LoginManager
import userManagement as dbHandler
from userManagement import User
import secrets

api = Flask(__name__)
cors = CORS(api)
api.config["CORS_HEADERS"] = "Content-Type"
api.config["SECRET_KEY"] = secrets.token_hex(16)
login_manager = LoginManager()
login_manager.init_app(api)

@login_manager.user_loader
def load_user(user_id):
    user = dbHandler.get_user_by_id(user_id)
    if user:
        return User(user.id, user.email, user.password, user.otp_secret, user.api_key, user.api_key_expiration)
    return None


limiter = Limiter(
    get_remote_address,
    app=api,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

def check_api_key():
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        api_key = auth_header.split(" ")[1]
        user = dbHandler.get_user_by_column("UsA17_api_key", api_key)
        if user and user.api_key == api_key:
            login_user(User(user.id, user.email, user.password, user.otp_secret, user.api_key, user.api_key_expiration))
            return None
    return jsonify({"error": "Invalid API key"}), 401


@api.route("/get_entry", methods=["GET"])
@limiter.limit("3/second", override_defaults=False)
def get_entry():
    api_key_error = check_api_key()
    if api_key_error:
        return api_key_error
    
    column_name = request.args.get('column_name')
    value = request.args.get('value')
    allowed_columns = {
        'Nzdvy_developer': 'developer',
        'hBbdT_project': 'project',
        '16Yh5_start_time': 'start_time',
        'MbOId_end_time': 'end_time',
        'Aiiyt_repo_url': 'repo_url',
        'LaH8Y_dev_note': 'dev_note',
        'qVKdx_code_snippet': 'code_snippet',
        'xI1ka_language': 'language',
        'vTJWO_time_worked': 'time_worked',
        'FVtfU_owner': 'owner'
    }
    if column_name:
        # Find the salted column name
        salted_column_name = None
        for salted, unsalted in allowed_columns.items():
            if unsalted == column_name:
                salted_column_name = salted
                break
        
        if not salted_column_name:
            raise ValueError(f"Invalid column name: {column_name}")
        
        data = dbHandler.get_diaries_by_column(salted_column_name, value)
    else:
        data = dbHandler.list_diaries()

    return jsonify(data), 200


@api.route("/add_entry", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def add_entry():
    api_key_error = check_api_key()
    if api_key_error:
        return api_key_error
    data = request.get_json()
    data["owner"] = current_user.id
    response, statuscode = dbHandler.insert_diaries_api(data)
    return jsonify(response), statuscode


if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=3000)