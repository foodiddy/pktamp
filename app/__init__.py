import os
from flask import Flask, render_template
from .api import api_bp
from .config import logger

def create_app():
    app_dir = '/opt/pktamp'
    static_folder = os.path.join(app_dir, 'static')
    
    app = Flask(__name__, static_folder=static_folder, static_url_path='/static')
    
    # Configure Jinja2 to use Vue.js-style delimiters
    app.jinja_env.variable_start_string = '{{{'
    app.jinja_env.variable_end_string = '}}}'
    
    app.register_blueprint(api_bp, url_prefix="/api")
    
    @app.route("/")
    def index():
        return render_template("index.html")
    
    logger.info("Flask app created")
    return app

app = create_app()
