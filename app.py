import datetime
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, current_user, logout_user
from static.forms.registration import RegForm
from static.forms.login import LoginForm
from static.data.users import User
from static.data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SoftHub'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    db_session.global_init("static/databases/softhub.db")
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

    if current_user.is_authenticated:
        return render_template('index.html',
                               title='SoftHUB | Проект о том, как развить SoftSkills',
                               user=current_user,
                               ip_addr=ip_addr)
    return render_template('index.html',
                           ip_addr=ip_addr)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegForm()
    user = User()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html',
                                   title='SoftHUB | Регистрация',
                                   form=form,
                                   email_error=f'Почта -- {form.email.data} -- занята!')
        else:
            user.email = form.email.data
            user.set_password(form.password.data)
            user.created_date = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S')

            db_sess.add(user)
            db_sess.commit()
            return 'Вы зарегистрировались!'
    return render_template('registration.html',
                           title='Регистрация',
                           form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user)
                return redirect('/')
            return render_template('login.html',
                                   form=form,
                                   error='Неверный пароль!',
                                   title='SoftHUB | Авторизация')
        return render_template('login.html',
                               form=form,
                               error='Аккаунта с таким логином не существует!',
                               title='SoftHUB | Авторизация')
    return render_template('login.html',
                           form=form,
                           title='SoftHUB | Проект о том, как развить SoftSkills')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    app.run()
