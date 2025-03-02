from django.db import models
from shortuuidfield import ShortUUIDField
# Create your models here.

class Department(models.Model):
    """
    sakura-admin系统部门表模型的
    """
    id = ShortUUIDField(primary_key=True, verbose_name='主键')
    name = models.CharField(max_length=128, verbose_name='部门名称')
    leader = models.CharField(max_length=128, blank=True, verbose_name='部门领导')
    rank = models.IntegerField(default=999, verbose_name='部门排序')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='child_departments', verbose_name='上级部门')
    remark = models.CharField(max_length=128, blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'system_department'
        verbose_name = '部门表'
        verbose_name_plural = verbose_name
        ordering = ['rank']

