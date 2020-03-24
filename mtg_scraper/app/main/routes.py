from flask import render_template
from app.main import bp
from app.models import User
from flask_login import login_required


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html')

@bp.route('/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user, cards=user.cards)

# @bp.route('/<username>/cards')
# @login_required
# def cards(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     return render_template('cards.html', cards=user.cards)

@bp.route('/edit_profile')
@login_required
def edit_profile():
    return 'edit profile page'


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))