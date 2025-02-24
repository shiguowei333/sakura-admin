# Generated by Django 5.1.6 on 2025-02-24 17:49

import shortuuidfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False, verbose_name='主键')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='角色名称')),
                ('sign', models.CharField(max_length=128, unique=True, verbose_name='角色标识')),
                ('remark', models.CharField(max_length=200, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('menus', models.ManyToManyField(blank=True, to='menu.menu', verbose_name='菜单/权限')),
            ],
            options={
                'verbose_name': '角色表',
                'verbose_name_plural': '角色表',
            },
        ),
    ]
