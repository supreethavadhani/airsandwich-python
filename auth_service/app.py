from flask import Flask
from config import config
from database import db
from routes import auth_bp
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config)

# Initialize DB
db.init_app(app)
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")

if __name__ == "__main__":
    app.run(port=5001, debug=config.DEBUG)