from flask import Blueprint, request, jsonify
from database import get_user_by_id
from flasgger import swag_from

users_bp = Blueprint('users', __name__)

@users_bp.route('/users/<user_id>', methods=['GET'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Get a specific user by ID',
    'description': 'Retrieves user details based on the provided user ID.',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'required': True,
            'type': 'string',
            'example': '123'
        }
    ],
    'responses': {
        '200': {
            'description': 'User found successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'string'},
                    'name': {'type': 'string'},
                    'email': {'type': 'string'}
                }
            }
        },
        '404': {
            'description': 'User not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def get_user_route(user_id):
    """
    Fetch a single user by ID.
    """
    try:
        user = get_user_by_id(user_id)

        if not user:
            return jsonify({"status": "error", "message": "No logs found for this user"}), 404

        return jsonify(logs), 200
    except Exception as e:
        print(f"Error fetching logs for user {user_id}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500