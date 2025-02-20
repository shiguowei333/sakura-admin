# 对drf的响应进行二次封装类

from rest_framework.response import Response
from rest_framework import status

# 基础通用响应，默认返回200，符合restful规范
class SakuraResponse(Response):
    def __init__(self, code=200, success=True, data=None, message=None, status=status.HTTP_200_OK, template_name=None, headers=None, exception=False, content_type=None):
        new_data = {"code": code, "success": success, "data": data, "messsge": message}
        super().__init__(new_data, status, template_name, headers, exception, content_type)