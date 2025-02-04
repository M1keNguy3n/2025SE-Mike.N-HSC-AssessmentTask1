from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import userManagement as dbHandler
from werkzeug.security import check_password_hash
import base64
from flask_login import current_user, LoginManager
from userManagement import User

api = Flask(__name__)
cors = CORS(api)
api.config["CORS_HEADERS"] = "Content-Type"

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
        user = dbHandler.get_user_by_api_key(api_key)
        if user and user.api_key == api_key:
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
    allowed_columns = ['developer', 'project', 'start_time', 'end_time', 'repo_url', 'dev_note', 'code_snippet', 'language']
    
    if column_name != None:
        if column_name not in allowed_columns:
            raise ValueError(f"Invalid column name: {column_name}")
    
    
    if column_name and value:
        data = dbHandler.get_diaries_by_column(column_name, value)
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
    response = dbHandler.insert_diaries_api(data)
    return response, 201


if __name__ == "__main__":
    api.run(debug=False, host="0.0.0.0", port=3000)