# 对drf的响应进行二次封装

from rest_framework.response import Response
from rest_framework import status

"""
    基础通用响应，封装符合restful规范的json数据格式
    code: 业务状态码
    success: 执行成功/失败
    message: 提示信息
    data: 执行成功返回数据
"""
class BaseResponse(Response):
    def __init__(self, code, success, message, data=None, status=status.HTTP_200_OK, template_name=None, headers=None, exception=False, content_type=None):
        json_data = {
            "code": code,
            "success": success,
            "message": message
        }
        if data is not None:
            json_data["data"] = data
        super().__init__(json_data, status, template_name, headers, exception, content_type)


# 标准响应成功的返回，业务码默认为1
class SuccessResponse(BaseResponse):
    def __init__(self, data=None, message='处理请求成功！', status=status.HTTP_200_OK):
        super().__init__(1, True, message, data, status)


# 标准响应失败的返回，业务码默认返回0，自定义返回data数据和message
class FailureResponse(BaseResponse):
    def __init__(self, message='处理请求失败！', status=status.HTTP_400_BAD_REQUEST):
        super().__init__(0, False, message, status)

class UnauthorizedResponse(BaseResponse):
    def __init__(self, message='令牌校验失败！', status=status.HTTP_401_UNAUTHORIZED):
        super().__init__(0, False, message, status)

class UnPermission:
    def __init__(self, message='权限不足！', status=status.HTTP_403_FORBIDDEN):
        super().__init__(0, False, message, status)