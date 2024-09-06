from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, Label, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    flag = Label(field_id='cmd_name', text='Название команды')
    try_ = SubmitField('TRY')
