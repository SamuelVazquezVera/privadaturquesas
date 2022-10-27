import functools
from flask import (
    render_template,
    Blueprint,
    flash,
    g,
    redirect,
    request,
    session,
    url_for
)

index = Blueprint('index', __name__)
@index.route("/")
def indexs():
    return redirect(url_for('auth.login'))