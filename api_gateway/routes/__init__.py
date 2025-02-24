from flask import Blueprint

# Import Blueprints AFTER defining Blueprint to avoid circular imports
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp

# Create a main Blueprint
main_bp = Blueprint("main", __name__)

# Register individual microservice Blueprints
main_bp.register_blueprint(auth_bp, url_prefix="/auth")
main_bp.register_blueprint(user_bp, url_prefix="/user")

# Function to register all routes in `app.py`
def register_routes(app):
    app.register_blueprint(main_bp)
