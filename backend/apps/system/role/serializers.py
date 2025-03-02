from rest_framework import serializers

from .models import Role
from ..menu.models import Menu


class RoleSerializer(serializers.ModelSerializer):

    menus = serializers.PrimaryKeyRelatedField(many=True, queryset=Menu.objects.all(), required=False)

    class Meta:
        model = Role
        fields = ['id', 'name', 'code', 'menus', 'remark']