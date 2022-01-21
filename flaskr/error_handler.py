from flask import (
    Blueprint, render_template
)

bp = Blueprint('error', __name__)

@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

