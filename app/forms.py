from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from app.models import User

class Authorization(FlaskForm):
    mail = EmailField('Электропочта', validators=[
        DataRequired('Введите email'),
        Email('Такого email не существует')],
        render_kw={'autofocus': True})
    password = PasswordField('Пароль', validators=[
        DataRequired('Введите пароль')
    ])
    submit = SubmitField('Войти')