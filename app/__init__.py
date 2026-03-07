from flask import Flask, render_template
from .api import api_bp
from .config import logger

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.register_blueprint(api_bp, url_prefix="/api")
    
    @app.route("/")
    def index():
        return render_template("index.html")
    
    logger.info("Flask app created")
    return app

app = create_app()
