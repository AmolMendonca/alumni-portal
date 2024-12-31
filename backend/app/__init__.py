from flask import Flask, jsonify
from flask_cors import CORS
import certifi
from pymongo import MongoClient
import logging
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_class=Config):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configurationfi
    app.config.from_object(config_class)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": config_class.CORS_ORIGINS,
            "methods": config_class.CORS_METHODS,
            "allow_headers": config_class.CORS_ALLOWED_HEADERS,
            "expose_headers": ["Content-Type"]
        }
    })
        
    with app.app_context():
        # Initialize MongoDB
        try:
            app.mongodb_client = MongoClient(
                Config.MONGO_URI,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=5000
            )
            
            app.database = app.mongodb_client[Config.MONGO_DB_NAME]
            app.mongodb_client.admin.command('ping')
            logger.info("Connected to MongoDB!")
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {str(e)}")
            raise
        
    @app.teardown_appcontext
    def close_mongo(exception):
        """close mongo when ap shutting down"""
        if hasattr(app, 'mongodb_client'):
            app.mongodb_client.close()
            logger.info("Closed MongoDB connection")
    
    # Register blueprints and error handlers
    register_blueprints(app)
    register_error_handlers(app)
    
    return app

def register_blueprints(app):
    """Register Flask blueprints"""
    try:
        from app.routes.search import create_search_blueprint
        from app.routes.profile import create_profile_blueprint
        
        profile_bp = create_profile_blueprint(app.database)
        search_bp = create_search_blueprint(app.database)
        
        app.register_blueprint(search_bp, url_prefix='/api/v1/search/')
        app.register_blueprint(profile_bp, url_prefix='/api/v1/profiles/')
        
        logger.info("Blueprints registered successfully")
    except Exception as e:
        logger.error(f"Error registering blueprints: {str(e)}")
        raise

def register_error_handlers(app):
    """Register error handlers"""
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "status": "error",
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500