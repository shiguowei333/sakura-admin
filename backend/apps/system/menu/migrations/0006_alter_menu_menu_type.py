# Generated by Django 5.1.6 on 2025-03-02 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_alter_menu_table_alter_menumeta_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='menu_type',
            field=models.SmallIntegerField(choices=[(0, '菜单'), (1, 'iframe'), (2, '外链'), (3, '按钮')], verbose_name='菜单类型'),
        ),
    ]
