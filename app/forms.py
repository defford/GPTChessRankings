from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from app.models import Player
from datetime import date

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PlayerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    rating = IntegerField('Initial Rating', default=1500, validators=[NumberRange(min=0, max=3000)])
    submit = SubmitField('Add Player')

    def validate_name(self, field):
        if Player.query.filter_by(name=field.data).first():
            raise ValidationError('Player name already exists. Please use a different name.')

class GameForm(FlaskForm):
    player1 = SelectField('Player 1', coerce=int, validators=[DataRequired()])
    player2 = SelectField('Player 2', coerce=int, validators=[DataRequired()])
    winner = SelectField('Winner', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], default=date.today)
    submit = SubmitField('Record Game')

    def validate_player2(self, field):
        if field.data == self.player1.data:
            raise ValidationError('Player 2 must be different from Player 1.')

    def validate_date(self, field):
        if field.data > date.today():
            raise ValidationError('Game date cannot be in the future.')