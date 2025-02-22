from flask import request, jsonify, Blueprint
from database import log_event
from flasgger import swag_from

logging_bp = Blueprint('logging', __name__)

@logging_bp.route('/log', methods=['POST'])
@swag_from({
    'tags': ['Logging'],
    'summary': 'Log an event',
    'description': 'Receives an event and logs the event.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'timestamp': {
                        'type': 'string',
                        'example': 1708401940
                        },
                    'event': {
                        'type': 'string',
                        'example': 'User logged in'
                        },
                    'data': {
                        'type': 'integer',
                        'example': {
                            'userID': 12345,
                            }
                        }
                },
                'required': ['message', 'timestamp']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Event logged successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'logged'}
                }
            }
        },
        '400': {
            'description': 'Invalid input'
        },
        '500': {
            'description': 'Internal server error'
        }
    }
})
def log_event_route():
    data = request.json

    try:
        log_event(data)
        return jsonify({"status": "logged"}), 200
    except Exception as e:
        print(f"Error in logging event: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
