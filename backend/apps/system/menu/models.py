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
        LINK = 2, "外链"
        BUTTON = 3, "按钮"


    id = ShortUUIDField(primary_key=True, verbose_name='主键')
    parent = models.ForeignKey('self', related_name="children_menu", on_delete=models.PROTECT, verbose_name="上级菜单", null=True, blank=True)
    route_name = models.CharField(max_length=128, blank=True, verbose_name="路由名称/外链")
    menu_type = models.SmallIntegerField(choices=MenuTypeChoices, verbose_name="菜单类型")
    code = models.CharField(max_length=128, blank=True, verbose_name="权限标识")
    route_path = models.CharField(max_length=255, blank=True, verbose_name="路由地址")
    component = models.CharField(max_length=255, blank=True, verbose_name="组件路径")
    redirect = models.CharField(max_length=128, blank=True, verbose_name="重定向地址")
    meta = models.OneToOneField('MenuMeta', on_delete=models.CASCADE, verbose_name="菜单元数据")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "菜单/权限表"
        verbose_name_plural = verbose_name
        db_table = 'system_menu'
        ordering = ("create_time",)


class MenuMeta(models.Model):
    """
    菜单/权限表元数据模型
    """
    class AnimationTypeChoices(models.TextChoices):
        BOUNCE = "bounce", "bounce"
        FLASH = "flash", "flash"
        PULSE = "pulse", "pulse"
        RUBBER_BAND = "rubberBand", "rubberBand"

    id = ShortUUIDField(primary_key=True, verbose_name='主键')
    title = models.CharField(max_length=128, verbose_name="菜单名称")
    icon = models.CharField(max_length=128, blank=True, verbose_name="菜单图标")
    rank = models.IntegerField(default=99, verbose_name="菜单排序")
    enter_animation = models.CharField(max_length=128, blank=True, verbose_name="进入动画")
    leave_animation = models.CharField(max_length=128, blank=True, verbose_name="离开动画")
    is_show = models.BooleanField(verbose_name="是否显示", default=True)
    parent_is_show = models.BooleanField(verbose_name='父级菜单是否显示', default=True)
    is_keepalive = models.BooleanField(max_length=128,default=True, verbose_name="是否缓存页面")
    fixed_tag = models.BooleanField(verbose_name="固定标签", default=False)
    iframe_url = models.CharField(max_length=128, blank=True, verbose_name="iframe链接地址")
    iframe_loading = models.BooleanField(default=True, verbose_name="iframe加载动画")
    is_hidden_tag = models.BooleanField(verbose_name="隐藏标签名", default=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "菜单/权限表元数据"
        verbose_name_plural = verbose_name
        db_table = 'system_menu_meta'
        ordering = ("-create_time",)