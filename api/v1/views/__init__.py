#!/usr/bin/python3
"""
Views for the AirBnB Clone v3 API
"""

from flask import Blueprint

# Create a Blueprint object for the API views
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import all view modules to register their routes
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
