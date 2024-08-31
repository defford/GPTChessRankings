from flask import Blueprint, render_template
from app.models import Player, Game
from flask_login import login_required

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/rankings')
def rankings():
    players = Player.query.order_by(Player.rating.desc()).all()
    return render_template('rankings.html', players=players)

@bp.route('/player/<int:player_id>')
def player_profile(player_id):
    player = Player.query.get_or_404(player_id)
    recent_games = Game.query.filter((Game.player1_id == player_id) | (Game.player2_id == player_id)).order_by(Game.date.desc()).limit(5).all()
    return render_template('player_profile.html', player=player, recent_games=recent_games)

@bp.route('/game-history')
def game_history():
    games = Game.query.order_by(Game.date.desc()).limit(20).all()
    return render_template('game_history.html', games=games)