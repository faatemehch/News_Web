# Generated by Django 3.1.7 on 2021-04-13 04:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news_blog_post', '0006_auto_20210411_2151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='categories_post',
        ),
        migrations.AddField(
            model_name='post',
            name='categories_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='news_blog_post.postcategory', verbose_name='دسته بندی خبر'),
        ),
    ]