#!/usr/bin/python3
"""Main Flask application"""

from flask import Flask
from api.v1.views.index import app_views
from models import storage

app = Flask(__name__)

# Register the app_views blueprint with the Flask app
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_storage(exception):
    """Close the SQLAlchemy session"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
