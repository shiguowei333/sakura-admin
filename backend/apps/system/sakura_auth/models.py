from datetime import timezone

from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin
from django.db import models
from shortuuidfield import ShortUUIDField


# Create your models here.



class SakuraUser(AbstractBaseUser, PermissionsMixin):
    """
    重写django默认的用户模型，自定义sakura-admin系统用户模型
    """
    uid = ShortUUIDField(primary_key=True, verbose_name='主键')
    username = models.CharField(max_length=150, unique=True, verbose_name='用户名')
    realname = models.CharField(max_length=150, verbose_name='真实姓名')
    email = models.CharField(max_length=150, unique=True, null=True, verbose_name='邮箱')
    mobile = models.CharField(max_length=150,unique=True, null=True, verbose_name='手机号')
    avatar = models.CharField(max_length=150, verbose_name='用户头像')
    is_active = models.BooleanField(default=True, verbose_name='用户状态')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
