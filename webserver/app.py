from flask import Flask
from flask_cors import CORS
from routes import register_blueprints
from flasgger import Swagger

port = 8001
ip_address = "0.0.0.0"

app = Flask(__name__)
CORS(app)
register_blueprints(app)
swagger = Swagger(app)

if __name__ == '__main__':
    app.run(host=ip_address, port=port, debug=True)

