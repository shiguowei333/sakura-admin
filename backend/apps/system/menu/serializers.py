from rest_framework import serializers

from .models import Menu, MenuMeta


class MenuMetaSerializer(serializers.ModelSerializer):
    """
    菜单meta序列化器
    """

    showLink = serializers.BooleanField(source="is_show")
    showParent = serializers.BooleanField(source="parent_is_show")
    keepAlive = serializers.BooleanField(source="is_keepalive")
    frameSrc = serializers.CharField(source="iframe_url", allow_null=True, required=False)
    frameLoading = serializers.BooleanField(source="iframe_loading", allow_null=True, required=False)
    hiddenTag = serializers.BooleanField(source="is_hidden_tag")
    fixedTag = serializers.BooleanField(source="fixed_tag")
    # 入场/出场动画数据自定义格式
    transition = serializers.SerializerMethodField()

    class Meta:
        model = MenuMeta
        fields = ["id", "title", "icon", "rank", "showLink", "showParent", "keepAlive", "frameSrc", "frameLoading", "hiddenTag", "fixedTag", "transition"]

    def get_transition(self, obj):
        return {
            "enterTransition": obj.enter_animation,
            "leaveTransition": obj.leave_animation
        }


class MenuSerializer(serializers.ModelSerializer):
    meta = MenuMetaSerializer()
    parent = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all(), allow_null=True)

    class Meta:
        model = Menu
        fields = ["id", "route_name", "route_path", "menu_type", "component", "code", "meta", "parent", "redirect"]



class RouteSerializer(serializers.ModelSerializer):
    """
    返回动态路由序列化器
    """
    meta = serializers.SerializerMethodField()  # 嵌套 MenuMeta 的序列化器
    parent = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all(), allow_null=True)

    name = serializers.CharField(source="route_name",  required=False)
    path = serializers.CharField(source="route_path", required=False)

    class Meta:
        model = Menu
        fields = ["id", "name", "path", "menu_type", "component", "code", "meta", "parent", "redirect"]

    def get_meta(self, obj):
        # 获取权限字典，从上下文中提取
        permission_dict = self.context.get("permission_dict", {})
        # 获取meta序列化对象
        meta_serializer = MenuMetaSerializer(obj.meta)

        # 清洗meta数据，去除空值的key-value
        meta_data = {key: value for key, value in meta_serializer.data.items() if value not in [None, "", [], {}]}

        # 添加 roles 列表
        meta_data["roles"] = [role.code for role in obj.roles.all()]
        # 添加 auth 列表
        if obj.id in permission_dict:
            meta_data["auths"] = permission_dict.get(obj.id)

        return meta_data

    def to_representation(self, instance):
        # Serialize the main instance data
        representation = super().to_representation(instance)
        # Filter out empty fields from the main data
        return {key: value for key, value in representation.items() if value not in [None, "", [], {}]}