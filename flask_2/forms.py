from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Неккоректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=16, message="Пароль должен быть от 4 до 16 символов")])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")
