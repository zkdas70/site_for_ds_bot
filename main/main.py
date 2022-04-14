from flask import Flask, render_template, redirect, request, make_response, \
    session, abort, jsonify
from data import db_session
from data.users_default import UsersDefault
from data.tasks import Tasks
from data.servers import Servers
from data.users_to_servers import UsersToServers
from data.task_to_servers import TaskToServers
from forms.user import LoginFormDefault, RegisterFormDefault
from forms.news import NewsForm
from flask_login import LoginManager, login_user, current_user, logout_user, \
    login_required
import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(UsersDefault).get(user_id)


@app.route("/")
def index():  # опа а где sql?
    param = {}
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user_name = current_user.name
        servers = dict()  # ansver.server
        for ansver in db_sess.query(UsersToServers).filter(UsersToServers.users == current_user.id).all():
            server = db_sess.query(Servers).filter(Servers.id == ansver.server).first()
            server_name = server.name
            server_id = server.id
            server_coins = ansver.coins + ansver.coins_cange
            is_admin = ansver.is_admin
            servers[server_name] = (
                server_coins,
                is_admin,
                server_id,
            )
        param['is_login'] = current_user.is_authenticated
        param['username'] = user_name
        param['servers'] = servers
        param['is_admin'] = None
        param['status'] = None
    return render_template("index.html", **param)


@app.route('/server_menejment/<int:id>', methods=['GET', 'POST'])
def server_menejment(id):
    param = {}
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        if db_sess.query(UsersToServers).filter(UsersToServers.users == current_user.id,
                                                UsersToServers.server == id).first().is_admin:
            users = []
            tasks = {}
            for i in db_sess.query(UsersDefault).filter(UsersToServers.server == id).all():
                users.append(f'{i.name} ({i.tag.split("#")[1]})')
            for i in db_sess.query(Tasks).filter(TaskToServers.server == id).all():
                tasks['name'] = i.name
                tasks['task'] = i.task
                tasks['ansver'] = i.ansver
                tasks['coins'] = i.coins
                tasks['created_date'] = i.created_date
            param['users'] = users
            param['tasks'] = tasks
            return render_template("server_menejment.html", **param)
        return render_template('access_denied.html')
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def reqister_user():
    invalid_characters_in_field = {'@', '"', "'", '!', '?', '/', '\\', '|', ',', '.',
                                   '!', '=', '-', '+', '&', '%', '$', ':', ';', '*'}
    form = RegisterFormDefault()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register_default.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(UsersDefault).filter(UsersDefault.tag == form.tag.data).first():
            return render_template('register_default.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if len(form.tag.data.split('#')) != 2 or len(form.tag.data.split('#')[1]) != 4:
            return render_template('register_default.html', title='Регистрация',
                                   form=form,
                                   message="введите дискорд ник и тег (имя#0000)")
        if not str(form.tag.data.split('#')[1]).isdigit():
            return render_template('register_default.html', title='Регистрация',
                                   form=form,
                                   message="некоректныйй тэг")
        if set(list(form.tag.data)) & invalid_characters_in_field:
            return render_template('register_default.html', title='Регистрация',
                                   form=form,
                                   message="введите коректный дискорд ник")
        user = UsersDefault(
            tag=form.tag.data,
            name=form.tag.data.split('#')[0],
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register_default.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFormDefault()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(UsersDefault).filter(
            UsersDefault.tag == form.tag.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login_default.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login_default.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()
