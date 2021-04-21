# Generated by Django 3.1.7 on 2021-04-11 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_blog_post', '0005_auto_20210411_2144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ManyToManyField(blank=True, null=True, to='news_blog_post.PostImage', verbose_name='تصویر خبر'),
        ),
    ]
