from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

OLLAMA_URL = "http://localhost:11434/api/generate"  
MODEL_NAME = "llama3.2:latest" 

@app.route('/')
def hello_world():
    return render_template('test.html') 

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    data = request.json
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # TODO implement streaming
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False}
        )
        response.raise_for_status()
        result = response.json()

        return jsonify({"suggestions": [result["response"]]})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001, debug=True)

