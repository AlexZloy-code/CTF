from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    name = EmailField('Название команды', validators=[DataRequired()])
    submit = SubmitField('Войти')