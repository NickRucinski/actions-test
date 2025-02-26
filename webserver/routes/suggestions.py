from flask import Blueprint, request, jsonify
import requests
from flasgger import swag_from

suggestions_bp = Blueprint('suggestions', __name__)

OLLAMA_URL = "http://localhost:11434/api/generate"  
DEFAULT_MODEL_NAME = "copilot-style-codellama:latest"

commands = [
    "Only respond with the code following the prompt.",
    "Do not point out mistakes.",
    "Respond in only plane text.",
    "Do not include text describing or explaining the code mistake at all",
    "Provide comments only where necessary.",
    "Do not provide additional information.",
    "If the prompt asks for an error, introduce a small syntax or logic mistake in the code. Do not explain or provide any extra context."
]

good_command = "<Prompt>Complete the following code:"
bad_command = "<Prompt>Complete the following code but introduce a small syntax or logic mistake:"

end_prompt = "</Prompt>"

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
    model_name = data.get("model", DEFAULT_MODEL_NAME)
    is_correct = data.get("isCorrect", True)

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:

        full_prompt = (
            "".join(commands) + (good_command if is_correct else bad_command) + prompt + end_prompt
        )

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model_name,
                "prompt": full_prompt,
                "keep_alive": "1h",
                "stream": False
            },
        )
        response.raise_for_status()
        result = response.json()

        return jsonify({"suggestions": [result["response"]]})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500