from app.models.errors import StatusCodes
from flask import jsonify
from enum import Enum



class StatusCodes(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501


def success_response(
        message: str,
        data=None,
        status_code: StatusCodes = StatusCodes.OK
):
    return jsonify({
        "status": "Success",
        "message": message,
        "data": data,
    }), status_code


def error_response(
        message: str,
        data=None,
        status_code: StatusCodes = StatusCodes.NOT_FOUND
):
    return jsonify({
        "status": "Error",
        "message": message,
        "data": data,
    }), status_code