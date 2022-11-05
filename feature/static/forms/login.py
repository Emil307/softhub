from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Почта',
                       validators=[DataRequired(message='Это поле обязательно!')],
                       name='email',
                       id='email',
                       render_kw={
                           'placeholder': "Почта"
                       }
                       )
    password = StringField('Пароль',
                           validators=[DataRequired(message='Это поле обязательно!')],
                           name='password',
                           id='password',
                           render_kw={
                               'placeholder': "Пароль"
                           }
                           )

