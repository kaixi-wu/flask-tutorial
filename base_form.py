from pydantic import BaseModel as pydanticBaseModel, Field
from typing import Union, Optional, Any
from flask import g, request
from sqlalchemy import sql
from sqlalchemy import or_

from base_model import BaseModel


def required_str_field(*args, **kwargs):
    """ 必传字段, 且长度大于1，防止传null、空字符串 """
    kwargs["min_length"] = 1
    return Field(..., **kwargs)


class BaseForm(pydanticBaseModel):
    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getattr__(self, item):
        return self.__dict__[item]

    def __init__(self):
        g.current_form = self
        request_data = request.get_json(silent=True) or request.get_data() or request.args.to_dict()
        super(BaseForm, self).__init__(**request_data)

        self.depends_validate()  # 自动执行有关系的依赖

    def depends_validate(self):
        """
        有依赖关系的数据验证，由于pydantic的验证顺序不可控，而业务上是存在字段先后和依赖关系的，所以统一重写此方法，在此方法内进行对应的验证
        """

    @classmethod
    def get_filed_title(cls, filed):
        """get 字段 title"""
        filed_obj = cls.model_fields.get(filed)
        return filed_obj.title if filed_obj else filed

    @classmethod
    def validate_data_is_exist(cls, db_model, msg: str = f'数据不存在', **kwargs):
        """校验数据是否存在"""
        data = db_model.query.filter_by(**kwargs).first()
        if data is None:
            raise ValueError(msg)
        return data

    @classmethod
    def validate_data_is_not_exist(cls, db_model, msg: str = f'数据已存在', **kwargs):
        """ 校验数据不存在 """
        if db_model.get_first(**kwargs):
            raise ValueError(msg)

    @classmethod
    def validate_data_or_is_not_exist(cls, db_model, msg: str = "数据已存在", **kwargs):
        """ 批量校验数据不存在 """
        if db_model.get_data_or_list(**kwargs):
            raise ValueError(msg)

    @classmethod
    def validate_is_true(cls, data, msg):
        if not data:
            raise ValueError(msg)

    @classmethod
    def validate_is_false(cls, data, msg):
        if data:
            raise ValueError(msg)

    @classmethod
    def validate_data_length(cls, data: Any, min_length, max_length, msg=None):
        if min_length < len(data) < max_length:
            return True
        else:
            raise ValueError(msg)


class PaginationForm(BaseForm):
    """ 分页的模型 """
    page_num: Optional[int] = Field(None, title="页数")
    page_size: Optional[int] = Field(None, title="页码")
    detail: bool = Field(False, title='是否获取详情')

    def get_query_filter(self, *args, **kwargs):
        """ 解析分页条件，此方法需重载 """
        return []
