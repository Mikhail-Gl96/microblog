from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    msgNoData = 'Необходимо ввести даные в поле'
    username = StringField('Логин', validators=[DataRequired(msgNoData)])
    password = PasswordField('Пароль', validators=[DataRequired(msgNoData)])
    remember_me = BooleanField('Запомнить вход')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    msgNoData = 'Необходимо ввести даные в поле'
    username = StringField('Логин', validators=[DataRequired(msgNoData)])
    email = StringField('Email', validators=[DataRequired(msgNoData), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(msgNoData)])
    password_repeat = PasswordField('Повторите пароль', validators=[DataRequired(msgNoData), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            msgLoginExists = 'Такой логин уже используется.\nПожалуйста, выберите другой'
            raise ValidationError(msgLoginExists)

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            msgEmailExists = 'Такой Email уже используется.\nПожалуйста, выберите другой'
            raise ValidationError(msgEmailExists)
