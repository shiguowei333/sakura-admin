import json
import os.path
from application.settings import BASE_DIR
from django.core.management.base import BaseCommand
from apps.system.menu.models import Menu, MenuMeta
from apps.system.role.models import Role
from apps.system.user.models import User


class Command(BaseCommand):
    help = '初始化核心数据（幂等操作）'

    def handle(self, *args, **kwargs):

        with open(os.path.join(BASE_DIR, 'apps\\system\\user\\management\\commands\\menu.json'), 'r', encoding='utf-8') as f:
            menu_data = json.load(f)
        # 系统菜单配置初始化
        # system菜单创建
        system_obj = menu_data[0]
        system_menu = Menu.objects.create(
            route_name = system_obj['router_name'],
            menu_type = system_obj['menu_type'],
            route_path = system_obj['route_path'],
            meta = MenuMeta.objects.create(title = system_obj['meta']['title'], icon = system_obj['meta']['icon'])
        )
        # system子菜单创建
        for menu in menu_data[0]['children']:
            Menu.objects.create(
                route_name = menu['router_name'],
                menu_type = menu['menu_type'],
                route_path = menu['route_path'],
                component = menu['component'],
                parent = system_menu,
                meta = MenuMeta.objects.create(title = menu['meta']['title'], icon = menu['meta']['icon'])
            )

        # 初始化超管角色，超管角色拥有所有菜单权限
        admin_role = Role.objects.create(
            name = '系统管理员',
            code = 'admin'
        )
        admin_role.menus.set(Menu.objects.all())

        # 初始化超管用户，超管用户默认为超管角色
        admin_user = User.objects.create(
            username = 'admin',
            name = '超级管理员'
        )
        admin_user.roles.set([admin_role])
        admin_user.set_password('admin123')
        admin_user.save()
        # 输出结果
        self.stdout.write(
            self.style.SUCCESS('系统初始化完成')
        )
