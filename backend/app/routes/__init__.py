from flask import Blueprint
# Import blueprints but don't register them here
from .search import create_search_blueprint
from .profile import create_profile_blueprint