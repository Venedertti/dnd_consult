import os
import logging
from flask import Flask
from src.database import db
from src.controller.spell_controller import spell_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise ValueError("Environment variable 'SQLALCHEMY_DATABASE_URI' is not set.")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    logging.basicConfig(level=logging.INFO)
    app.logger.info('Flask app is starting with database URI: %s', app.config['SQLALCHEMY_DATABASE_URI'])

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(spell_bp, url_prefix='/spells')

    return app
