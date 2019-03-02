from flask import Blueprint, jsonify

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(400)
def error_400(error):
    message = {
        "error": "Client error"
    }

    return jsonify(message), 400


@errors.app_errorhandler(500)
def error_500(error):
    message = {
        "error": "Server error"
    }
    return jsonify(message), 500

