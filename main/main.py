from random import choice
from flask import Flask, render_template, redirect, request, make_response, \
    session, abort, jsonify
from data import db_session
from data.users_default import UsersDefault
from data.tasks import Tasks
from data.servers import Servers
from data.users_to_servers import UsersToServers
from data.task_to_servers import TaskToServers
from forms.user import LoginFormDefault, RegisterFormDefault
from forms.task import TaskForm
from flask_login import LoginManager, login_user, current_user, logout_user, \
    login_required
import datetime
import json

DEBAG = True


def generate_secret_key():
    if DEBAG:
        secret_key = '3ZnqU04e9vhaF8fyBD5W1QbJ'
    else:
        password_letters_0 = list('abcdefghijklmnpqorstuvwxyz')
        password_letters_1 = list('0123456789')
        password_letters_2 = list('ABCDEFGHIJKLMNPQORSTUVWXYZ')
        secret_key = set()
        for i in range(10):
            secret_key.add(choice(password_letters_0))
            secret_key.add(choice(password_letters_1))
            secret_key.add(choice(password_letters_2))
        secret_key = ''.join(secret_key)
    return secret_key


app = Flask(__name__)
app.config['SECRET_KEY'] = generate_secret_key()
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
            server_coins = ansver.coins
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


@app.route('/server_menejment/<int:id>', methods=['GET', 'POST'])
def server_menejment(id):
    param = {}
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        if db_sess.query(UsersToServers).filter(UsersToServers.users == current_user.id,
                                                UsersToServers.server == id).first().is_admin:
            users = []
            tasks = []
            for user_id in db_sess.query(UsersToServers).filter(UsersToServers.server == id).all():
                users.append(f'{db_sess.query(UsersDefault).filter(UsersDefault.id == user_id.users).first().name}')
            for tasks_to_server in db_sess.query(TaskToServers).filter(TaskToServers.server == id).all():
                task = dict()
                task_answer = db_sess.query(Tasks).filter(Tasks.id == tasks_to_server.task).first()
                if task_answer:
                    task['id'] = task_answer.id
                    task['name'] = task_answer.name
                    task['task'] = task_answer.task
                    task['coins'] = task_answer.coins
                    task['answer'] = task_answer.answer
                    task['creator'] = task_answer.creator
                    task['is_private'] = task_answer.is_private
                    task['created_date'] = task_answer.created_date
                    tasks.append(task)
            param['users'] = users
            param['tasks'] = tasks
            param['server_id'] = id
            param['current_user'] = current_user
            return render_template("server_menejment.html", **param)
        return render_template('access_denied.html')
    return redirect("/")


@app.route('/add_tasks', methods=['GET', 'POST'])
@app.route('/add_tasks/<int:server_id>', methods=['GET', 'POST'])
def add_tasks(server_id=None):
    if current_user.is_authenticated:
        form = TaskForm()
        param = dict()
        if server_id:
            param['value_is_private'] = True
        else:
            param['value_is_private'] = False
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            tasks = Tasks()
            tasks.name = form.name.data
            tasks.task = form.task.data
            tasks.coins = form.coins.data
            tasks.answer = form.answer.data
            tasks.creator = current_user.id
            tasks.is_private = form.is_private.data
            db_sess.add(tasks)
            db_sess.commit()
            if server_id:
                if db_sess.query(UsersToServers).filter(UsersToServers.users == current_user.id,
                                                        UsersToServers.server == server_id).first().is_admin:
                    task_to_servers = TaskToServers()
                    task_to_servers.server = server_id
                    task_to_servers.task = tasks.id
                    db_sess.add(task_to_servers)
                    db_sess.commit()
                    return redirect(f'/server_menejment/{server_id}')
                return render_template('access_denied.html')
            return redirect('/')
        return render_template('add_task.html', **param, title='Добавление задания', form=form)
    return redirect('/login')


@app.route('/edit_tasks/<int:task_id>', methods=['GET', 'POST'])
@app.route('/edit_tasks/<int:task_id>/<int:server_id>', methods=['GET', 'POST'])
def edit_tasks(task_id, server_id=None):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        form = TaskForm()
        if db_sess.query(Tasks).filter(Tasks.id == task_id).first():
            param = dict()
            tasks_answer = db_sess.query(Tasks).filter(Tasks.id == task_id).first()
            if tasks_answer:
                param['server_id'] = server_id
                param['value_name'] = tasks_answer.name
                param['value_task'] = tasks_answer.task
                param['value_coins'] = tasks_answer.coins
                param['value_answer'] = tasks_answer.answer
                param['value_is_private'] = tasks_answer.is_private
            if form.validate_on_submit():
                is_creator_menejment = db_sess.query(Tasks).filter(Tasks.creator == current_user.id,
                                                                   Tasks.id == task_id).all()
                if len(is_creator_menejment) == 1:
                    is_creator_menejment = True
                else:
                    is_creator_menejment = False
                is_admin_menejment = db_sess.query(Tasks).filter(Tasks.is_private == True,
                                                                 Tasks.id == task_id).all()
                is_admin_menejment += db_sess.query(TaskToServers).filter(TaskToServers.server == server_id,
                                                                          TaskToServers.task == task_id).all()
                if len(is_admin_menejment) == 2:
                    is_admin_menejment = True
                else:
                    is_admin_menejment = False
                is_admin = db_sess.query(UsersToServers).filter(UsersToServers.users == current_user.id,
                                                                UsersToServers.server == server_id).all()
                if len(is_admin) == 1:
                    is_admin = True
                else:
                    is_admin = False
                if (is_admin_menejment and is_admin) or is_creator_menejment:
                    tasks = db_sess.query(Tasks).filter(Tasks.id == task_id).first()
                    tasks.name = form.name.data
                    tasks.task = form.task.data
                    tasks.answer = form.answer.data
                    tasks.coins = form.coins.data
                    if not server_id:
                        tasks.is_private = False
                    else:
                        tasks.is_private = form.is_private.data
                    db_sess.add(tasks)
                    db_sess.commit()
                    if server_id:
                        return redirect(f'/server_menejment/{server_id}')
                    return redirect(f'/')
                param['task_cannot_be_changed'] = True
            return render_template('add_task.html', **param, title='изменить задания', form=form)
        return render_template('access_denied.html')
    return redirect(f'/login')


@app.route(f'/delete_tasks/<int:task_id>', methods=['GET', 'POST'])
@app.route(f'/delete_tasks/<int:task_id>/<int:server_id>', methods=['GET', 'POST'])
@login_required
def delete_tasks(task_id, server_id=None, is_deleting_only_from_server=None):
    db_sess = db_session.create_session()
    task = db_sess.query(Tasks).filter(Tasks.id == task_id, Tasks.creator == current_user.id).first()
    if not task and db_sess.query(TaskToServers).filter(TaskToServers.server == server_id,
                                                        TaskToServers.task == task_id).first():
        task = db_sess.query(Tasks).filter(Tasks.id == task_id, Tasks.is_private == True).first()
    if task:
        if not is_deleting_only_from_server:
            servers_to_users = db_sess.query(TaskToServers).filter(TaskToServers.task == task_id).all()
            for server_to_user in servers_to_users:
                db_sess.delete(server_to_user)
        db_sess.delete(task)
        db_sess.commit()
        if server_id:
            return redirect(f'/server_menejment/{server_id}')
        return redirect(f'/')
    abort(404)


@app.route(f'/delete_tasks_from_server/<int:task_id>/<int:server_id>', methods=['GET', 'POST'])
@login_required
def delete_tasks_from_server(task_id, server_id):
    db_sess = db_session.create_session()
    task = db_sess.query(TaskToServers).filter(TaskToServers.task == task_id, TaskToServers.server == server_id).first()
    if task:
        db_sess.delete(task)
        db_sess.commit()
        return redirect(f'/server_menejment/{server_id}')
    abort(404)


@app.route('/public_tasks')
def public_tasks():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        param = dict()
        servers = []
        tasks = []
        for task_answer in db_sess.query(Tasks).filter(Tasks.is_private == False).all():
            task = dict()
            task['id'] = task_answer.id
            task['name'] = task_answer.name
            task['task'] = task_answer.task
            task['coins'] = task_answer.coins
            task['answer'] = task_answer.answer
            task['creator'] = task_answer.creator
            task['is_private'] = task_answer.is_private
            task['created_date'] = task_answer.created_date
            tasks.append(task)
        param['tasks'] = tasks
        for server_answer in db_sess.query(UsersToServers).filter(UsersToServers.is_admin == True).all():
            server = dict()
            server['server_name'] = db_sess.query(Servers).filter(Servers.id == server_answer.server).first().name
            server['server_id'] = server_answer.server
            servers.append(server)
        param['servers'] = servers
        param['current_user'] = current_user
        return render_template("public_tasks.html", **param)
    return render_template("index.html")


@app.route('/add_task_to_server/<int:task_id>/<int:server_id>')
def add_task_to_server(task_id, server_id):
    db_sess = db_session.create_session()
    if db_sess.query(UsersToServers).filter(UsersToServers.users == current_user.id,
                                            UsersToServers.server == server_id).first().is_admin:
        task_to_servers = TaskToServers()
        task_to_servers.server = server_id
        task_to_servers.task = task_id
        db_sess.add(task_to_servers)
        db_sess.commit()
        return redirect(f'/server_menejment/{server_id}')
    return render_template('access_denied.html')


@app.route('/refresh')
def refresh():
    app.config['SECRET_KEY'] = generate_secret_key()
    return 'refresh completed'


def main():
    db_session.global_init("db/blogs.db", )
    app.run(debug=DEBAG)


if __name__ == '__main__':
    main()
