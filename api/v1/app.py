#!/usr/bin/python3
"""Script that imports a Blueprint and runs Flask."""

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv

from api.v1.views import app_views
from models import storage
from flasgger import Swagger

app = Flask(__name__)

# Register API blueprint
app.register_blueprint(app_views)

# Configure CORS
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# Configure Swagger
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "Flasgger",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
    "specs": [
        {
            "version": "1.0",
            "title": "HBNB API",
            "endpoint": 'v1_views',
            "description": 'HBNB REST API',
            "route": '/v1/views',
        }
    ]
}
swagger = Swagger(app)

@app.teardown_appcontext
def teardown_session(exception):
    """Closes storage session."""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Handles 404 Not Found errors."""
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == '__main__':
    # Get host and port from environment variables or use defaults
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    
    # Run Flask app
    app.run(host=host, port=port, threaded=True)
