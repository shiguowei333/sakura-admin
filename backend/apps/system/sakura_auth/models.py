from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from shortuuidfield import ShortUUIDField
from django.contrib.auth.hashers import make_password


# Create your models here.

class SakuraUserManager(BaseUserManager):
    """
    自定义sakura-admin系统用户模型的manager类
    """
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        初始化用户相关功能
        """
        if not username:
            raise ValueError("必须设置用户名！")

        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, password=None, **extra_fields):
        """
        暂时不增加超级管理员的概念，权限相关暂时使用认证登录即可，后续增加RBAC权限相关的内容
        """
        return self._create_user(username, password, **extra_fields)


class SakuraUser(AbstractBaseUser):
    """
    重写django默认的用户模型，自定义sakura-admin系统用户模型
    """
    uid = ShortUUIDField(primary_key=True, verbose_name='主键')
    username = models.CharField(max_length=150, unique=True, verbose_name='用户名')
    name = models.CharField(max_length=150, verbose_name='姓名/昵称')
    telephone = models.CharField(max_length=150,unique=True, verbose_name='电话号码')
    avatar = models.CharField(max_length=150, blank=True, verbose_name='用户头像')
    email = models.CharField(max_length=150, blank=True, verbose_name='邮箱')
    is_active = models.BooleanField(default=True, verbose_name='用户状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = SakuraUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
