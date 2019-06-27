from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    msgNoData = 'Необходимо ввести даные в поле'
    username = StringField('Логин', validators=[DataRequired(msgNoData)])
    password = PasswordField('Пароль', validators=[DataRequired(msgNoData)])
    remember_me = BooleanField('Запомнить вход')
    submit = SubmitField('Войти')
