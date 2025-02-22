from flask import Blueprint, request, jsonify

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
    get_user_by_id()
    if response.data:
        return jsonify(response.data[0]), 200
    return jsonify({"error": "User not found"}), 404