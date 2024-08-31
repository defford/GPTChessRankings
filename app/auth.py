from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Player, Game
from app.forms import LoginForm, PlayerForm, GameForm
from datetime import date
from app.elo import update_ratings
from urllib.parse import urlparse

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/admin')
@login_required
def admin():
    return render_template('admin/dashboard.html')

@bp.route('/admin/manage_players', methods=['GET', 'POST'])
@login_required
def manage_players():
    form = PlayerForm()
    if form.validate_on_submit():
        player = Player(name=form.name.data, rating=form.rating.data)
        db.session.add(player)
        db.session.commit()
        flash('Player added successfully', 'success')
        return redirect(url_for('auth.manage_players'))
    players = Player.query.all()
    return render_template('admin/manage_players.html', form=form, players=players)

@bp.route('/admin/record_game', methods=['GET', 'POST'])
@login_required
def record_game():
    form = GameForm()
    form.player1.choices = [(p.id, p.name) for p in Player.query.order_by('name')]
    form.player2.choices = [(p.id, p.name) for p in Player.query.order_by('name')]
    form.winner.choices = [(-1, 'Draw')] + form.player1.choices
    if form.validate_on_submit():
        player1 = Player.query.get(form.player1.data)
        player2 = Player.query.get(form.player2.data)
        winner = Player.query.get(form.winner.data) if form.winner.data != -1 else None
        
        game = Game(
            player1=player1,
            player2=player2,
            winner=winner,
            date=form.date.data
        )
        db.session.add(game)
        
        update_ratings(player1, player2, winner)
        
        db.session.commit()
        flash('Game recorded successfully', 'success')
        return redirect(url_for('auth.record_game'))
    return render_template('admin/record_game.html', form=form)

@bp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500