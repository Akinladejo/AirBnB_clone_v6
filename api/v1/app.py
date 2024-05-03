#!/usr/bin/python3
"""app Module"""
from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv
from models import storage
from api.v1.views import app_views

# Create Flask app instance
app = Flask(__name__)

# Enable CORS for all origins
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# Register blueprints
app.register_blueprint(app_views)

# Disable strict slashes in URLs
app.url_map.strict_slashes = False

# Set jsonify to pretty print JSON responses
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Retrieve host and port from environment variables, fallback to defaults
host = getenv("HBNB_API_HOST", "0.0.0.0")
port = int(getenv("HBNB_API_PORT", 5000))


@app.teardown_appcontext
def close_storage(exception):
    """Calls storage.close() at the end of the request"""
    storage.close()


@app.errorhandler(404)
def handle_404_error(error):
    """Handles 404 errors by returning a JSON-formatted response"""
    return jsonify({"error": "Not found"}), 404


# Run the Flask app
if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
