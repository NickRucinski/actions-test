from flask import render_template, Blueprint
from flasgger import swag_from

main_page_bp = Blueprint('main_page', __name__)

@main_page_bp.route('/')
def main_page_route():
    try:
        return render_template('test.html')
    except Exception as e:
        return f"Error loading page: {str(e)}", 500