# Generated by Django 2.1.4 on 2018-12-31 10:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0007_auto_20181231_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 31, 10, 29, 23, 849278), verbose_name='主机注册时间'),
        ),
        migrations.AlterField(
            model_name='hostgroup',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 31, 10, 29, 23, 849796), verbose_name='主机组注册时间'),
        ),
    ]
