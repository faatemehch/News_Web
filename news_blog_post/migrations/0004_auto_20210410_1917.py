# Generated by Django 3.1.7 on 2021-04-10 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_blog_post', '0003_auto_20210408_1704'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment_post',
            options={'ordering': ['-date_added'], 'verbose_name': 'نظر کاربر', 'verbose_name_plural': 'نظرات کاربران'},
        ),
    ]
