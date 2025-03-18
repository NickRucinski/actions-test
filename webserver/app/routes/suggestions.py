from flask import Blueprint, request
from app.services.suggestion_service import getSuggestion
from app.models.response import *
from app.models.status_codes import StatusCodes
from flasgger import swag_from

suggestions_bp = Blueprint('suggestions', __name__)

@suggestions_bp.route('/suggestion', methods=['POST'])
@swag_from({
    'tags': ['Suggestions'],
    'summary': 'Generate a suggestion using the AI model',
    'description': 'Sends a prompt to the locally running Ollama model with an optional model name and correctness flag, returning the generated suggestion.',
    'consumes': ['application/json'],
    'produces': ['application/json'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'prompt': {
                        'type': 'string',
                        'example': 'def add(a, b):'
                    },
                    'vendor': {
                        'type': 'string',
                        'example': "ollama"
                    },
                    'model': {
                        'type': 'string',
                        'example': 'codellama:7b',
                        'description': 'The AI model to use for generating the suggestion.'
                    },
                    'isCorrect': {
                        'type': 'boolean',
                        'example': False,
                        'description': 'A flag indicating whether the suggestion should be correct.'
                    }
                },
                'required': ['prompt']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Successfully generated suggestion',
            'schema': {
                'type': 'object',
                'properties': {
                    'suggestions': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'example': ["return a + b"]
                    }
                }
            }
        },
        '400': {
            'description': 'Bad Request - No prompt provided',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'No prompt provided'}
                }
            }
        },
        '500': {
            'description': 'Internal Server Error - Failed to generate response',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Connection error'}
                }
            }
        }
    }
})
def generate_suggestion_route():
    """
    Generate a suggestion based on the provided prompt.
    See Swagger docs for more information.
    """
    data = request.json
    prompt = data.get("prompt", "")
    vendor_name = data.get("vendor")
    model_name = data.get("model")
    model_params = data.get("params")
    is_correct = data.get("is_correct")

    if not prompt:
        return error_response(
            "No prompt provided",
            None,
            StatusCodes.BAD_REQUEST
        )

    try:
        # Call getSuggestion with all parameters, it will decide which model to use
        response = getSuggestion(
            prompt=prompt,
            vendor=vendor_name,
            model_name=model_name,
            model_params=model_params,
            is_correct=is_correct
        )
        return success_response(
            "AI Suggestions",
            { "suggestions": [response]},
            StatusCodes.OK
        )
    
    except Exception as e:
        return error_response(
            str(e),
            None,
            StatusCodes.SERVER_ERROR
        )