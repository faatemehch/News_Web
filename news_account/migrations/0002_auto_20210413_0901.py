# Generated by Django 3.1.7 on 2021-04-13 04:31

import datetime
from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('news_account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='date_added',
            field=django_jalali.db.models.jDateTimeField(blank=True, default=datetime.datetime(2021, 4, 13, 9, 1, 23, 297455), null=True, verbose_name='تاریخ ثبت نام کاربر'),
        ),
    ]
