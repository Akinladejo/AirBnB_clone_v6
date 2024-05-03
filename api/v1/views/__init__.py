#!/usr/bin/python3
""" Initializes the API v1 views """

from flask import Blueprint

# Import modules without importing their contents
from api.v1.views import index
from api.v1.views import states
from api.v1.views import cities
from api.v1.views import amenities
from api.v1.views import users
from api.v1.views import places
from api.v1.views import places_reviews
from api.v1.views import places_amenities

# Create a Blueprint object for API v1 views
app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")

# Register blueprints from imported modules
app_views.register_blueprint(index.app_views)
app_views.register_blueprint(states.app_views)
app_views.register_blueprint(cities.app_views)
app_views.register_blueprint(amenities.app_views)
app_views.register_blueprint(users.app_views)
app_views.register_blueprint(places.app_views)
app_views.register_blueprint(places_reviews.app_views)
app_views.register_blueprint(places_amenities.app_views)
