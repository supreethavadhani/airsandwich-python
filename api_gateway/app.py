from flask import Flask
import logging
from dotenv import load_dotenv
from config import config
from routes import register_routes

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

# Configure logging
logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Register all routes from `routes/`
register_routes(app)

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
