import jwt
import random
import string

from flask import current_app as app
from werkzeug.security import check_password_hash
from base_model import BaseModel
from exts import db


class Role(BaseModel):
    __abstract__ = False
    __tablename__ = 'auth_role'
    __table_args__ = {"comment": "角色信息表"}
    role_name = db.Column(db.String(80), unique=True, nullable=False, comment="角色名称")
    parent_role_id = db.Column(db.Integer, nullable=True, comment="父级角色")
    frontend = db.Column(db.Text, comment="前端权限")
    Backend = db.Column(db.Text, comment="后端权限")
    enable = db.Column(db.Boolean, default=True, comment="启用状态，1禁用，0启用")

    def __repr__(self):
        return f'<Role: {self.role_name}>'

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
