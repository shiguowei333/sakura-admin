from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from utils.response import SuccessResponse, FailureResponse, UnauthorizedResponse
from .serializers import LoginReqSerializer, UserSerializer
from ..menu.models import Menu
from ..menu.serializers import RouteSerializer


# 生成菜单树形结构
def build_tree(data: list, parent_val=None, id_key='id', parent_key='parent') -> list:
    """
    通用树形结构生成器
    :param data: 原始扁平数据列表
    :param parent_val: 当前父节点值（自动识别）
    :param id_key: ID字段名
    :param parent_key: 父ID字段名
    :return: 标准树形结构
    """
    tree = []
    for item in data.copy():
        if item.get(parent_key) == parent_val:
            data.remove(item)
            children = build_tree(data, item[id_key], id_key, parent_key)
            if children:
                item['children'] = children
            # temp_item = item.copy()
            # temp_item.pop(parent_key, None)
            # tree.append(temp_item)
            tree.append(item)
    return tree



# Create your views here.
# 登录视图
class LoginView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginReqSerializer(data=request.data)
        # 登录参数序列化器校验
        if not serializer.is_valid():
            return FailureResponse(message=serializer.errors)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        # 登录校验
        user = authenticate(username=username, password=password)
        if user is None:
            return UnauthorizedResponse(message='用户名或密码错误')
        # 获取token
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        # 计算过期时间
        current_time = timezone.now()
        expiration_time = current_time + access_token.lifetime
        expiration_time_str = expiration_time.strftime("%Y-%m-%d %H:%M:%S")
        user_data = UserSerializer(user).data
        # 获取用户角色信息
        roles = user.roles.all()
        data = {
            'avatar': user_data['avatar'],
            'username': user_data['username'],
            'nickname': user_data['name'],
            'roles': [role.code for role in roles],
            'accessToken': str(access_token),
            'refreshToken': str(refresh),
            'expires': expiration_time_str
        }
        return SuccessResponse(data=data, message='登录成功！')

# 刷新令牌视图
class RefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        current_time = timezone.now()

        # 调用父类的 post 方法来获取默认的响应
        try:
            # 获取原始数据
            response = super().post(request, *args, **kwargs)
            original_data = response.data
            access_token = original_data.get('access')
            refresh_token = original_data.get('refresh')

            # 计算访问令牌的到期时间
            access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            expiration_time = current_time + access_token_lifetime
            expiration_time_str = expiration_time.strftime('%Y-%m-%d %H:%M:%S')

            data = {
                'accessToken': access_token,
                'refreshToken': refresh_token,
                'expires': expiration_time_str
            }

            return SuccessResponse(data=data, message="令牌刷新成功！")
        except:
            # 处理错误响应
            return UnauthorizedResponse(message="令牌已失效！")


class AsyncRoutesView(APIView):
    def get(self, request):
        user = request.user
        roles = user.roles.all()
        # 根据用户角色获取所有关联的菜单、外链、内嵌，避免重复通过 distinct 去重
        menus = Menu.objects.filter(role__in=roles, menu_type__in=(Menu.MenuTypeChoices.MENU, Menu.MenuTypeChoices.IFRAME, Menu.MenuTypeChoices.LINK)).distinct().order_by("meta__rank")

        # 获取用户关联的所有按钮权限字，并按照 parent_id 进行分组
        permissions = Menu.objects.filter(role__in=roles, menu_type=Menu.MenuTypeChoices.BUTTON).distinct()
        # 将权限根据 parent_id 进行分组
        permission_dict = {}
        for perm in permissions:
            parent_id = perm.parent_id
            if parent_id not in permission_dict:
                permission_dict[parent_id] = []
            permission_dict[parent_id].append(perm.code)

        serializer = RouteSerializer(menus, many=True, context={"permission_dict": permission_dict})

        tree_data = build_tree(serializer.data)
        # 返回 JSON 响应
        return SuccessResponse(data=tree_data, message="动态路由获取成功")