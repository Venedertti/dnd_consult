import os
import logging
from flask import Flask
from src.database import db
from dotenv import load_dotenv
from src.controller.spell_controller import spell_bp
from src.controller.automate_controller import automate_bp

def create_app():
    app = Flask(__name__)
    load_dotenv()
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {'options': '-c timezone=UTC', 'client_encoding': 'UTF8'}
    }

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise ValueError("Environment variable 'SQLALCHEMY_DATABASE_URI' is not set.")
    
    logging.basicConfig(level=logging.INFO)
    
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(spell_bp, url_prefix='/spells')
    app.register_blueprint(automate_bp, url_prefix='/automate')

    return app
