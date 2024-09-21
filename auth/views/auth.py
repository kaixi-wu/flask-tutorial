from base_enum import UserStatus, ErrorMessage as errorMessage
from werkzeug.security import check_password_hash, generate_password_hash
from ..blueprint import auth_blue
from flask import current_app as app, request, jsonify, session, g
from ..models.auth import User
from ..models.role import Role
from exts import db
from utils.views import restful
from ..form.auth import LoginForm, UserListForm, RegisterForm, GetUserForm, ChangePasswordForm

import functools
import logging


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return jsonify({"success": False, "data": "登录信息已失效"})
        return view(**kwargs)

    return wrapped_view


@login_required
@auth_blue.post('/register')
def register():
    form = RegisterForm()
    User.model_create(form.model_dump())
    return app.restful.add_success()


"""
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            account = data.get('account')
        # print(f"data: {username}")
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif User.query.filter_by(username=username, delete=False).first():
            error = '用户已注册！'
        elif User.query.filter_by(email=email, delete=False).first():
            error = '用户已注册！'
        elif User.query.filter_by(account=account, delete=False).first():
            error = '用户已注册!'
        if error is None:
            try:
                new_user = User(username=username, email=email, account=account, password=generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()
                return "success"
            except Exception as e:
                return f"error: {e}"
    return error
    """


@auth_blue.post('/login')
def auth_login():
    form = LoginForm()
    user_info = form.user.to_dict(pop_list=['password'])
    user_info["access_token"] = form.user.build_access_token()
    session['user_id'] = user_info["id"]
    return app.restful.login_success(user_info)


"""
    error = None
    if request.method == 'POST':
        account = request.json.get('account')
        password = request.json.get('password')
        user = User.query.filter_by(account=account).first()

        if user is None:
            error = '用户未注册'
        elif not check_password_hash(user.password, password):
            error = '密码错误'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            # return redirect(url_for('login_success'))
            return app.restful.login_success("login success!")
    return jsonify({'error': error})
"""


@auth_blue.post('/refresh_token')
def auth_refresh_token():
    pass


@auth_blue.put('/logout')
def auth_logout():
    session.clear()
    return app.restful.logout_success()


@login_required
@auth_blue.put('/reset_password')
def auth_reset_password():
    """ 重置密码 """
    form = GetUserForm()
    new_password = form.user.reset_password()
    return app.restful.success(f'重置成功，新密码是: {new_password}')


""" 
    user_id = session.get('user_id')
    if request.method == 'POST':
        new_password = request.json.get('new_password')
        old_password = request.json.get('old_password')
        account = request.json.get('account')
        error = None
        if not new_password:
            error = 'new_password is required.'
        elif not old_password:
            error = 'old_password is required.'
        elif not account:
            error = 'account is required.'

        if not check_password_hash(g.user.password, old_password):
            return jsonify({"success": False, "data": "旧密码错误"})

        if old_password == new_password:
            return jsonify({"success": False, "data": "新密码不能与旧密码相同"})
        try:
            user = User.query.get(user_id)
            user.password = generate_password_hash(new_password)
            db.session.commit()
            return jsonify({"success": True, "data": "密码修改成功"})
        except Exception as e:
            db.session.rollback()
            logging.error(f"密码重置时出错: {e}")
            return jsonify({"success": False, "data": "密码修改失败"})

    return jsonify({"success": False, "data": "仅支持POST请求"})
"""


@auth_blue.put("/change_password")
def auth_change_password():
    """ 修改密码 """
    form = ChangePasswordForm()
    form.user.model_update({"password": form.new_password})
    return app.restful.success(f'密码修改成功')


@auth_blue.get('/list')
def auth_get_user_list():
    """ 获取用户列表 """
    form = UserListForm()
    get_filed = None
    if not form.detail:  # 获取用户详情列表
        get_filed = [
            User.id, User.username, User.account, User.status, User.create_time, User.create_user
        ]
    return app.restful.get_success(User.make_pagination(form, get_filed=get_filed))


@auth_blue.get("/role_list")
def auth_get_user_role_list():
    """ 获取用户的角色 """
    pass


@auth_blue.put("/update")
def auth_update_user():
    """ 修改用户 """
    pass
