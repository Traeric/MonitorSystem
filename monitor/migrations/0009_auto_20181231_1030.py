# Generated by Django 2.1.4 on 2018-12-31 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0008_auto_20181231_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='主机注册时间'),
        ),
        migrations.AlterField(
            model_name='hostgroup',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='主机组注册时间'),
        ),
    ]