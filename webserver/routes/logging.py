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
            'description': 'Bad request or invalid input',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'error'},
                    'message': {'type': 'string', 'example': 'Missing required fields: event, text'}
                }
            }
        },
        '500': {
            'description': 'Internal server error'
        }
    }
})
def log_event_route():
    data = request.json

    required_fields = ['timestamp', 'event', 'data']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"status": "error", "message": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    try:
        log_event(data)
        return jsonify({"status": "logged"}), 200
    except Exception as e:
        print(f"Error in logging event: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
