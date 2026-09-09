from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .routes.github_routes import github_bp
from .routes.api_routes import api_bp
from .routes.export_routes import export_bp
from .config import config
from .models.user_analytics import db
import os

# Initialize extensions
cache = Cache()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    """Application factory function"""
    app_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(os.path.dirname(app_dir), 'static')
    template_dir = os.path.join(app_dir, 'templates')
    
    app = Flask(__name__, 
                static_folder=static_dir,
                template_folder=template_dir)
    
    # Configuration
    app.config['DEBUG'] = config.DEBUG
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    
    # Cache configuration
    if config.CACHE_TYPE == 'redis':
        app.config['CACHE_TYPE'] = 'RedisCache'
        app.config['CACHE_REDIS_URL'] = config.CACHE_REDIS_URL
    elif config.CACHE_TYPE == 'filesystem':
        app.config['CACHE_TYPE'] = 'FileSystemCache'
        app.config['CACHE_DIR'] = 'cache'
    else:
        app.config['CACHE_TYPE'] = 'SimpleCache'
    
    app.config['CACHE_DEFAULT_TIMEOUT'] = config.CACHE_TIMEOUT
    
    # Rate limiting configuration
    app.config['RATELIMIT_STORAGE_URL'] = config.RATELIMIT_STORAGE_URL
    
    # Initialize extensions
    db.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    CORS(app, origins=config.CORS_ORIGINS)
    
    # Register blueprints
    app.register_blueprint(github_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(export_bp, url_prefix='/export')
    
    # Create database tables safely
    try:
        with app.app_context():
            db.create_all()
    except Exception as db_err:
        print(f"Warning: Database initialization skipped: {db_err}")
    
    return app
