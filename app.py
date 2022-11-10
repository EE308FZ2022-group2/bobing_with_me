from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, url_for, render_template, redirect, Flask, session, flash
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, login_required, current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp
from datetime import timedelta
import logging

import conf
from basic_user import get_user, create_user
from user_info import User

app = Flask(__name__, template_folder='./templates', static_folder='')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

cursor = conf.db.cursor()

app.secret_key = 'kaifeng'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)


class LoginForm(FlaskForm):
    """登录表单类"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64)])
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            ),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password_confirmation", message="Passwords must match."),
        ],
    )
    password_confirmation = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField(label="Register")


@login_manager.user_loader  # 定义获取登录用户的方法
def load_user(user_id):
    return User.get(user_id)


@app.route('/login', methods=['GET', 'POST'])  # 登录
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    emsg = None
    user_name = form.username.data
    password = form.password.data
    user_info = get_user(user_name)  # 从用户数据中查找用户记录
    if user_info is None:
        emsg = "please enter username or password"
        return render_template('login.html', err=emsg)
    else:
        user = User(user_info[0])  # 创建用户实体
        if check_password_hash(user.password_hash, password):  # 校验密码
            login_user(user)
            return redirect(url_for('index'))
        else:
            emsg = "username or password error!"
            return render_template('login.html', err=emsg)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    form = RegisterForm()
    sql = "insert into users(username, password, email, money) " \
          "VALUES ('%s', '%s', '%s', '%d')" % \
          (form.username.data, generate_password_hash(form.password.data), form.email.data, 0)
    try:
        cursor.execute(sql)
        conf.db.commit()

    except AttributeError:
        conf.e()
        logging.error(AttributeError)
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/rules', methods=['GET'])
@login_required
def rules():
    return render_template('rules.html')


@app.route('/multiplate', methods=['GET'])
@login_required
def mutiplater():
    return render_template('multiplater.html')


@app.route('/individual', methods=['GET'])
@login_required
def individual():
    get_point = request.args.get('point')
    sql = f"select money from users where username = '{current_user.username}'"
    try:
        cursor.execute(sql)
        conf.db.commit()
        result = cursor.fetchall()
        if result:
            plus = result[0][0] + int(get_point)
            sql_update = f"update users set money = '{plus}' where username = '{current_user.username}'"
            cursor.execute(sql_update)
            conf.db.commit()
    except Exception as e:
        conf.e()
        logging.error(e)

    return render_template('individual.html')


@app.route('/multi', methods=['GET'])
@login_required
def multi():
    return render_template('Muliti_Mode.html')


@app.route('/triple', methods=['GET'])
@login_required
def triple():
    return render_template('triple.html')


@app.route('/ranking', methods=['GET'])
@login_required
def ranking():
    sql = "select username, money from users order by money desc limit 5"
    try:
        cursor.execute(sql)
        conf.db.commit()
        result = cursor.fetchall()

    except Exception as e:
        conf.e()
        logging.error(e)
        return render_template('test.html')
    return render_template('ranking.html',
                           u1=result[0][0], m1=result[0][1],
                           u2=result[1][0], m2=result[1][1],
                           u3=result[2][0], m3=result[2][1],
                           u4=result[3][0], m4=result[3][1],
                           u5=result[4][0], m5=result[4][1]
                           )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5678, debug=True)
