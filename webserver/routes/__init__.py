from flask import Blueprint
from .suggestions import suggestions_bp
from .logging import logging_bp
from .main_page import main_page_bp

def register_blueprints(app):
    app.register_blueprint(suggestions_bp)
    app.register_blueprint(logging_bp)
    app.register_blueprint(main_page_bp)
