from flask import Blueprint, request, jsonify, Response, stream_with_context
import requests
import json

suggestions_bp = Blueprint('suggestions', __name__)

OLLAMA_URL = "http://localhost:11434/api/generate"  
MODEL_NAME = "llama3.2:latest" 

@suggestions_bp.route('/generate', methods=['GET', 'POST'])
def generate_suggestion_route():
    data = request.json
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    def generate_response():
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": True
            },
            stream=True
        )

        for line in response.iter_lines():
            if line:
                try:
                    yield f"data: {line.decode('utf-8')}\n\n"
                except json.JSONDecodeError as err:
                    print(f"Error decoding JSON: {err}")

    return Response(stream_with_context(generate_response()), content_type="text/event-stream")