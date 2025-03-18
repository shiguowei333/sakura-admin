from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.system.department.models import Department
from apps.system.role.models import Role

User = get_user_model()


# 登录请求序列化器，可以在此处添加登录表单的校验
class LoginReqSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

# 登录响应序列化器，格式化返回user表中需要的数据
class UserSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), required=False)
    roles = serializers.PrimaryKeyRelatedField(many=True, queryset=Role.objects.all(), required=False)
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'telephone', 'email', 'avatar', 'password', 'roles', 'department', 'is_active', 'create_time']


    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop('password', None)
        roles = validated_data.pop('roles', None)
        if roles is not None:
            instance.roles.set(roles)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance