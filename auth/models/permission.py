import jwt
import random
import string

from flask import current_app as app
from werkzeug.security import check_password_hash
from base_model import BaseModel
from exts import db

class Permissions(BaseModel):
    __abstract__ = False
    __tablename__ = 'auth_resource'
    __table_args__ = {"comment": "权限信息表"}
    resource_name = db.Column(db.String(80), unique=True, nullable=False, comment="权限名称")
    resource_type = db.Column(db.String(80), nullable=False, comment="权限类型")
    resource_classify = db.Column(db.String(80), nullable=False, comment="权限分类")
    resource_address = db.Column(db.String(200), unique=True, nullable=False, comment="权限地址")

    def __repr__(self):
        return f'<Role: {self.resource_name}>'


class UserRole(BaseModel):
    __abstract__ = False
    __tablename__ = 'auth_user_role'
    __table_args__ = {"comment": "用户角色关联表"}
    user_id = db.Column(db.Integer, nullable=False, comment="用户id")
    role_id = db.Column(db.Integer, nullable=False, comment="角色id")


class RolePermissions(BaseModel):
    __abstract__ = False
    __tablename__ = 'auth_role_res'
    __table_args__ = {"comment": "角色权限关联表"}
    role_id = db.Column(db.Integer, nullable=False, comment="角色id")
    res_id = db.Column(db.Integer, nullable=False, comment="权限id")
