from flask import Blueprint, request, jsonify
from app.services.suggestion_service import getSuggestion
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
                    'model': {
                        'type': 'string',
                        'example': 'llama3.2:latest',
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
    model_name = data.get("model", "ollama")
    temperature = data.get("temperature", 0.2)
    top_p = data.get("top_p", 1)
    top_k = data.get("top_k", 0)
    max_tokens = data.get("max_tokens", 256)
    is_correct = data.get("isCorrect", True)

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        # Call getSuggestion with all parameters, it will decide which model to use
        response = getSuggestion(
            prompt=prompt,
            model_name=model_name,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_tokens=max_tokens,
            is_correct=is_correct
        )

        return jsonify({"suggestions": [response["suggestions"]]})
    
    except Exception as e:
        print(f"Error fetching suggestion: {e}")
        return jsonify({"error": str(e)}), 500