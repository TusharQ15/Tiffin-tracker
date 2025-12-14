import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_seasurf import SeaSurf
from flask_session import Session
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
mail = Mail()
csrf = SeaSurf()

# Rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    Session(app)
    
    # Security headers
    Talisman(
        app,
        force_https=app.config['ENV'] == 'production',
        session_cookie_secure=True,
        strict_transport_security=True,
        content_security_policy={
            'default-src': ["'self'"],
            'script-src': [
                "'self'",
                'cdn.jsdelivr.net',
                'code.jquery.com',
                'cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'
            ],
            'style-src': [
                "'self'",
                'cdn.jsdelivr.net',
                'fonts.googleapis.com',
                'cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
                'cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css',
                "'unsafe-inline'"
            ],
            'img-src': [
                "'self'",
                'data:',
                'cdn.jsdelivr.net',
                'via.placeholder.com'
            ],
            'font-src': [
                "'self'",
                'fonts.gstatic.com',
                'cdn.jsdelivr.net',
                'data:'
            ]
        },
        content_security_policy_nonce_in=['script-src']
    )

    # Register blueprints
    from app.routes import main, auth, admin, api
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(admin.bp, url_prefix='/admin')
    app.register_blueprint(api.bp, url_prefix='/api/v1')

    # Error handlers
    from app.utils import errors
    app.register_error_handler(404, errors.not_found_error)
    app.register_error_handler(403, errors.forbidden_error)
    app.register_error_handler(500, errors.internal_error)

    # Shell context
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': models.User,
            'Order': models.Order,
            'Meal': models.Meal
        }

    return app

# Import models at the bottom to avoid circular imports
from app import models
