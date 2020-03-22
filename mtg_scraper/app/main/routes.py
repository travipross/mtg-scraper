from flask import render_template
from app.main import bp
from app.models import User

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@bp.route('/edit_profile')
def edit_profile():
    return 'edit profile page'