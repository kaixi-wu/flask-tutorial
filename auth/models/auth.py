import jwt
import random
import string

from flask import current_app as app
from werkzeug.security import check_password_hash
from base_model import BaseModel
from exts import db


class User(BaseModel):
    __abstract__ = False
    __tablename__ = 'auth_user'
    __table_args__ = {"comment": "用户基本信息表"}
    username = db.Column(db.String(80), unique=True, nullable=False, comment="用户名称")
    account = db.Column(db.String(80), unique=True, nullable=False, comment="用户账号")
    password = db.Column(db.String(256), nullable=False, comment="password")
    phone = db.Column(db.String(80), comment="电话")
    email = db.Column(db.String(120), comment="邮箱")
    status = db.Column(db.Boolean, default=True, comment="用户状态，1正常，2注销，3冻结")

    def __repr__(self):
        return f'<User: {self.username}>'

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def build_access_token(self):
        user_info = self.to_dict()
        user_info.pop("create_time")
        user_info.pop("update_time")
        # print(user_info)
        return jwt.encode(user_info, app.config["SECRET_KEY"])

    def to_dict(self, **kwargs):
        return super(User, self).to_dict(pop_list=["password"], filter_list=kwargs.get("filter_list", []))

    @classmethod
    def is_admin(cls):
        """ 用户是否是admin """
        return "admin" in cls.account

    def reset_password(self):
        """ 重置密码 """
        new_password = ''.join(random.sample(string.ascii_letters, 4))  # 随机字母
        new_password += ''.join(random.sample(string.punctuation, 2))  # 随机标点
        new_password += ''.join(random.sample(string.digits, 2))  # 随机数字
        new_password += ''.join(random.sample(string.ascii_letters, 4))  # 随机字母
        self.model_update({"password": new_password})
        return new_password