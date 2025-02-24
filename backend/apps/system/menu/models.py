from django.db import models
from shortuuidfield import ShortUUIDField
# Create your models here.


class Menu(models.Model):
    """
    sakura-admin系统菜单/权限表模型
    """
    class MenuTypeChoices(models.IntegerChoices):
        MENU = 0, "菜单"
        IFRAME = 1, "iframe"
        LINK = 3, "外链"
        BUTTON = 4, "按钮"

    class AnimationTypeChoices(models.TextChoices):
        BOUNCE = "bounce", "bounce"
        FLASH = "flash", "flash"
        PULSE = "pulse", "pulse"
        RUBBER_BAND = "rubberBand", "rubberBand"


    id = ShortUUIDField(primary_key=True, verbose_name='主键')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name="上级菜单", null=True, blank=True)
    name = models.CharField(max_length=128, verbose_name="菜单名称")
    menu_type = models.SmallIntegerField(choices=MenuTypeChoices, verbose_name="菜单类型")
    router_name = models.CharField(max_length=128, blank=True, verbose_name="路由名称")
    router_path = models.CharField(max_length=128, blank=True, verbose_name="路由路径")
    component = models.CharField(max_length=128, blank=True, verbose_name="组件路径")
    rank = models.IntegerField(default=999, verbose_name="菜单排序")
    router_redirect = models.CharField(max_length=128, blank=True, verbose_name='路由重定向地址')
    icon = models.CharField(max_length=128, blank=True, verbose_name="菜单图标")
    enter_animation = models.CharField(max_length=128, choices=AnimationTypeChoices, default=AnimationTypeChoices.BOUNCE, verbose_name="进入动画")
    leave_animation = models.CharField(max_length=128, choices=AnimationTypeChoices, default=AnimationTypeChoices.BOUNCE, verbose_name="离开动画")
    is_show = models.BooleanField(verbose_name="是否显示", default=True)
    parent_is_show = models.BooleanField(verbose_name='父级菜单是否显示')
    cache_page = models.BooleanField(max_length=128, verbose_name="缓存页面")
    fixed_tag = models.BooleanField(verbose_name="固定标签", default=False)
    iframe = models.CharField(max_length=128, blank=True, verbose_name="iframe链接地址")
    url = models.CharField(max_length=128, blank=True, verbose_name="外链地址")
    code = models.CharField(max_length=128, blank=True, verbose_name="权限标识")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')


    class Meta:
        verbose_name = "菜单/权限表"
        verbose_name_plural = verbose_name
        ordering = ("-rank","create_time")

