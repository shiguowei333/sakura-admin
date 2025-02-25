# Generated by Django 5.1.6 on 2025-02-26 14:12

import django.db.models.deletion
import shortuuidfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False, verbose_name='主键')),
                ('name', models.CharField(max_length=128, verbose_name='部门名称')),
                ('leader', models.CharField(blank=True, max_length=128, verbose_name='部门领导')),
                ('rank', models.IntegerField(default=999, verbose_name='部门排序')),
                ('department_level', models.IntegerField(default=0, verbose_name='部门层级')),
                ('remark', models.CharField(blank=True, max_length=128, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('parent_department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child_departments', to='department.department', verbose_name='上级部门')),
            ],
            options={
                'verbose_name': '部门表',
                'verbose_name_plural': '部门表',
                'db_table': 'system_department',
                'ordering': ['rank'],
            },
        ),
    ]
