from django.db.models import ProtectedError
from django.http import Http404
from rest_framework import exceptions
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, APIException
from rest_framework.views import exception_handler, set_rollback
from rest_framework_simplejwt.exceptions import InvalidToken

from utils.response import FailureResponse


def CustomExceptionHandler(exc, context):
    """
    统一处理API相关的异常关闭
    响应为标准错误响应
    异常情况比较多，如果碰到不明确的异常返回需要在这里补充判断
    """

    msg = ""
    response = exception_handler(exc, context)
    if isinstance(exc, AuthenticationFailed):
        if "User is inactive" in str(exc.detail):
            msg = "该账号已被禁用,请联系管理员"
        elif response and response.data.get("detail") == "Given token not valid for any token type":
            msg = "身份认证已过期"
        else:
            msg = exc.detail
    elif isinstance(exc, NotAuthenticated):
        msg = exc.detail
    elif isinstance(exc, exceptions.ValidationError):
        msg = exc.detail
        errorMsg = msg
        try:
            for key in errorMsg:
                if key:
                    msg = "%s:%s" % (key, errorMsg[key][0])
                else:
                    msg = errorMsg[key][0]
        except:
            if isinstance(errorMsg, list):
                msg = errorMsg[0]
            elif isinstance(errorMsg, dict):
                values_list = list(errorMsg.values())
                keys_list = list(errorMsg.keys())
                if "non_field_errors" in values_list[0]:
                    msg = keys_list[0] + ":" + values_list[0]["non_field_errors"][0]
                elif isinstance(values_list[0], list):
                    msg = keys_list[0] + ":" + values_list[0][0]
                else:
                    msg = errorMsg[0]
            else:
                msg = errorMsg
    elif "django.db.utils.IntegrityError" in str(type(exc)):
        msg = str(exc)
        res = msg.split(", ")
        if res[0] == "(1062":
            msg = "数据有重复，请检查后重试:%s" % msg
    elif isinstance(exc, Http404):
        msg = "404错误：您访问的地址不存在"
    elif isinstance(exc, APIException):
        set_rollback()
        msg = str(exc.detail)
    elif isinstance(exc, exceptions.APIException):
        set_rollback()
        msg = exc.detail
    elif isinstance(exc, ProtectedError):
        set_rollback()
        msg = "删除失败:该条数据与其他数据有相关绑定"
    elif isinstance(exc, Exception):
        msg = str(exc)  # 原样输出错误

    return FailureResponse(message=msg, status=response.status_code)