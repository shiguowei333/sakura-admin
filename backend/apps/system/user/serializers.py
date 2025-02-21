from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

# 登录请求序列化器，可以在此处添加登录表单的校验
class LoginReqSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

# 登录响应序列化器，格式化返回user表中需要的数据
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'name', 'avatar')
        extra_kwargs = {"password": {"write_only": True}}  # 设置密码为只写字段