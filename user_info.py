from flask_login import UserMixin  # 引入用户基类

import conf

cursor = conf.db.cursor()


class User(UserMixin):
    """用户类"""
    def __init__(self, user):
        self.username = user[1]
        self.password_hash = user[2]
        self.id = user[0]

    def verify_password(self, password):
        """密码验证"""
        if self.password_hash is None:
            return False
        return self.password_hash == password

    def get_id(self):
        """获取用户ID"""
        return self.id

    @staticmethod
    def get(user_id):
        """根据用户ID获取用户实体，为 login_user 方法提供支持"""
        if not user_id:
            return None
        sql = f'select * from users where id = {user_id}'
        try:
            cursor.execute(sql)
            conf.db.commit()
            result = cursor.fetchall()
            for user in result:
                if user[0] == user_id:
                    return User(user)
            return None

        except Exception as e:
            conf.e()
            print(e)

