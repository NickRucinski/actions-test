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

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
        )
        response.raise_for_status()
        result = response.json()

        return jsonify({"suggestions": [result["response"]]})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500