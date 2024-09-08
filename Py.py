import datetime
import sqlite3
import logging

from flask import Flask, Blueprint
from flask import render_template, redirect, request, make_response, jsonify, send_file, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.users import User
from data.jobs import Jobs

from forms.login_form import LoginForm
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/users.db")

# отключаем логирование
""" app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True """

blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


def chek_flag(flag):
    db_sess = db_session.create_session()
    if flag == 'null':
        con = sqlite3.connect("db/users.db")
        cur = con.cursor()
        cur.execute(
            f"""UPDATE users SET jobs = "{0}" WHERE id = {current_user.id}""").fetchall()
        con.commit()
        con.close()
    else:
        for i in db_sess.query(Jobs).all():
            if i.id not in current_user.jobs and flag == i.flag:
                con = sqlite3.connect("db/users.db")

                cur = con.cursor()

                cur.execute(
                    f"""UPDATE users SET jobs = "{current_user.jobs + i.id}" WHERE id = {current_user.id}""").fetchall()

                con.commit()

                con.close()

                current_user.jobs += i.id
                break


@app.route("/download/<path:filename>")
def get_csv(filename):
    try:
        return send_file('tasks/' + filename, as_attachment=True, download_name=filename)
    except FileNotFoundError:
        abort(404)


@app.route("/ball_changer/<path:command>/<path:balls>")
def ball_changer(command, balls):
    try:
        db_sess = db_session.create_session()
        con = sqlite3.connect("db/users.db")
        cur = con.cursor()
        cur.execute(
                f"""UPDATE users SET fine = {db_sess.query(User).filter(User.name == command)[0].fine - int(balls)} WHERE name = '{command}'""").fetchall()
        con.commit()
        con.close()
    except FileNotFoundError:
        abort(404)

    return render_template('CTF.html', title='CTF')


@app.route("/add/<path:command>")
def add(command):
    try:
        db_sess = db_session.create_session()
        con = sqlite3.connect("db/users.db")
        cur = con.cursor()
        try:
            if not list(db_sess.query(User).filter(User.name == command)):
                cur.execute(
                    f"""INSERT INTO users (
                          id,
                          name,
                          jobs,
                          fine
                      ) VALUES ({len(list(db_sess.query(User).all())) + 1}, "{command}", 0, 0)""").fetchall()
        except Exception as ex:
            print(ex)
        con.commit()
        con.close()
        return render_template('CTF.html', title='CTF')
    except FileNotFoundError:
        abort(404)


def create_route(i):
    @app.route(f'/{i.type.lower()}', endpoint=i.type)
    def index():
        return render_template('index1.html', job=i, current_user=current_user)


for i in db_session.create_session().query(Jobs).all():
    create_route(i)


@app.route('/', methods=['GET', 'POST'])
def main_website():
    if request.method == 'POST':
        chek_flag(request.form['input_flag'])

    return render_template('CTF.html', title='CTF')


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        if request.method == 'POST':
            chek_flag(request.form['input_flag'])

        jobs = db_sess.query(Jobs).all()

    else:
        jobs = []
    return render_template('index.html', title='Журнал работ', jobs=jobs, current_user=current_user)


@app.route('/rating', methods=['GET', 'POST'])
def rating():
    if request.method == 'POST':
        chek_flag(request.form['input_flag'])

    db_sess = db_session.create_session()

    table = []

    for i in db_sess.query(User).all():
        balls = db_sess.query(User).filter(User.id == i.id)[0].fine
        if int(i.jobs):
            for a in i.jobs[1:]:
                job = db_sess.query(Jobs).filter(Jobs.id == a)[0]
                balls += job.balls
        table.append([i.name, balls])

    return render_template('rating.html', table=sorted(table, key=lambda x: [-x[1], x[0]]))


@app.route('/web/web1')
def web1():
    return render_template('web1.html', title='web1')


@login_manager.user_loader
def load_user(user_id):
    return db_session.create_session().query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.name.data:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form.name.data).first()
        if user:
            login_user(user, remember=form.remember_me.data)
            return redirect("/tasks")
        return render_template('login.html',
                               message="Нет такой команды",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    app.register_blueprint(blueprint)
    app.run(port=8000, host='127.0.0.1')


if __name__ == '__main__':
    main()
