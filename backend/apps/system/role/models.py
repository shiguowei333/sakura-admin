from django.db import models
from shortuuidfield import ShortUUIDField
# Create your models here.

class Role(models.Model):
    """
    sakura-admin系统角色表模型
    """
    id = ShortUUIDField(primary_key=True, verbose_name='主键')
    name = models.CharField(max_length=128, unique=True, verbose_name='角色名称')
    sign = models.CharField(max_length=128, unique=True, verbose_name='角色标识')
    menus = models.ManyToManyField('menu.Menu', blank=True, verbose_name='菜单/权限')
    remark = models.CharField(max_length=200, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '角色表'
        verbose_name_plural = verbose_name
