# Generated by Django 5.1.6 on 2025-03-02 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telephone',
            field=models.CharField(max_length=128, verbose_name='电话号码'),
        ),
    ]
