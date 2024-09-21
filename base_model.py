from flask_sqlalchemy import SQLAlchemy, BaseQuery as _BaseQuery
from datetime import datetime
from flask import g
from sqlalchemy import or_
from werkzeug.security import generate_password_hash
from contextlib import contextmanager


class BaseQuery(_BaseQuery):

    def filter_by(self, **kwargs):
        kwargs.setdefault('delete', False)
        return super(BaseQuery, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=BaseQuery)


class BaseModel(db.Model):
    __table__ = None
    __abstract__ = True

    db = db

    # 基类模型
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="主键自增")
    delete = db.Column(db.Boolean, default=False, nullable=False, comment="是否删除")
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now(), comment="创建时间")
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now(),
                            comment="更新时间")
    create_user = db.Column(db.Integer(), nullable=True, default=None, comment="创建数据的用户id")
    update_user = db.Column(db.Integer(), nullable=True, default=None, comment="修改数据的用户id")
    remark = db.Column(db.String(80), comment="备注")

    @classmethod
    def get_first(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def get_data_or_list(cls, **kwargs):
        filters = [cls.__dict__[key] == value for key, value in kwargs.items()]
        return cls.query.filter(or_(*filters)).first()

    @classmethod
    def get_table_column_name_list(cls):
        return [column.name for column in cls.__table__.columns]

    def to_dict(self, pop_list: list = [], filter_list: list = []):
        if pop_list or filter_list:
            dict_data = {}
            for column_name in self.get_table_column_name_list():
                if filter_list:
                    if column_name in filter_list:
                        dict_data[column_name] = getattr(self, column_name)
                else:
                    if column_name not in pop_list:
                        dict_data[column_name] = getattr(self, column_name)
            return dict_data
        return {column.name: getattr(self, column.name, None) for column in self.__table__.columns}

    @classmethod
    def make_pagination(cls, form, get_filed=None, order_by=None, **kwargs):
        if get_filed is None:
            get_filed = []
        if get_filed is None:
            get_filed = cls.__table__.columns
        if order_by is None:
            order_by = cls.id
        col_name_list = [column.name for column in get_filed]  # 字段名称
        query_date = cls.db.session.query(*get_filed).filter(*form.get_query_filter(**kwargs)).order_by(order_by).all()
        return {
            "total": len(query_date),
            "data": [dict(zip(col_name_list, item)) for item in query_date]
        }

    @classmethod
    def format_insert_data(cls, data_dict):
        if "id" in data_dict:
            data_dict.pop("id")

        if cls.__name__ == "User" and "password" in data_dict:
            data_dict["password"] = generate_password_hash(data_dict["password"])

        try:  # 执行初始化脚本、执行测试时，不在上下文中，不能使用g对象
            if hasattr(g, 'user_id') and g.user_id:
                current_user = g.user_id  # 真实用户
            else:
                from auth.model_factory import User
                current_user = User.db.session.query(User.id).filter(User.account == "common").first()[0]
        except Exception as error:
            current_user = None
        data_dict["create_user"] = data_dict["update_user"] = current_user
        data_dict["create_time"] = data_dict["update_time"] = None

        # 只保留模型中有的字段
        return {key: value for key, value in data_dict.items() if key in cls.get_table_column_name_list()}

    @classmethod
    def auto_add(cls, insert_dict: dict):
        try:
            db.session.add(cls(**insert_dict))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        finally:
            db.session.close()

    @classmethod
    @contextmanager
    def auto_commit(cls):
        try:
            yield
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        finally:
            db.session.close()

    def model_update(self, data_dict: dict):
        """ 更新数据 """
        if "id" in data_dict:
            data_dict.pop("id")
        if self.__class__.__name__ == "User" and "password" in data_dict:
            data_dict["password"] = generate_password_hash(data_dict["password"])
        try:
            data_dict["update_user"] = g.user_id if hasattr(g, "user_id") else None
        except:
            pass
        with self.auto_commit():
            for key, value in data_dict.items():
                if hasattr(self, key):
                    setattr(self, key, value)

    @classmethod
    def model_create(cls, data_dict: dict):
        """ 创建数据 """
        insert_dict = cls.format_insert_data(data_dict)
        # print(insert_dict)
        cls.auto_add(insert_dict)
