from flask import Flask
from .api import api_bp
from .config import logger

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix="/api")
    
    @app.route("/")
    def index():
        return app.send_static_file("index.html")
    
    logger.info("Flask app created")
    return app

app = create_app()
