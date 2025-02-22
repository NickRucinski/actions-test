from flask import request, jsonify, Blueprint
from database import log_event
import time

logging_bp = Blueprint('logging', __name__)

@logging_bp.route('/log', methods=['POST'])
def log_event_route():
    data = request.json
    log_event(data)
    print(f"LOGGED EVENT: {data}")  # Print to console for debugging
    return jsonify({"status": "logged"}), 200
