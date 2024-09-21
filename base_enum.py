from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def get_value_tuple(cls):
        return (filed.value for filed in cls)


class AuthType(str, BaseEnum):
    """ 身份验证类型 """
    login = "login"
    permission = "permission"
    admin = "admin"
    not_auth = "not_auth"


class UserStatus(int, BaseEnum):
    NORMAL = 1
    CANCEL = 2
    FROZEN = 3


class ErrorMessage(str, BaseEnum):
    USER00001 = 'user.not.Registration'
