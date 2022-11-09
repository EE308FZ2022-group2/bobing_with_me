import logging
from init import login_manager

import conf
from user_info import User

cursor = conf.db.cursor()


def create_user(user_name, password, email):
    """创建一个用户"""
    sql = "insert into users(username, password, email, money) " \
          "VALUES ('%s', '%s', '%s', '%d')" % \
          (user_name, password, email, 0)
    try:
        cursor.execute(sql)
        conf.db.commit()

    except AttributeError:
        conf.e()
        logging.error(AttributeError)


def get_user(user_name):
    """根据用户名获得用户记录"""
    global result
    sql = f"select * from users where username = '{user_name}'"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        conf.db.commit()
        if not result:
            return None
        return result

    except Exception as e:
        conf.e()
        print(e)


@login_manager.user_loader  # 定义获取登录用户的方法
def load_user(user_id):
    return User.get(user_id)
