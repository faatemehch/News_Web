from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.db import models
import os
import datetime


def get_file_name_ext(file_path):
    base_name = os.path.basename( file_path )
    name, ext = os.path.splitext( base_name )
    return name, ext


def upload_image_path(instance, fileName):
    name, ext = get_file_name_ext( fileName )
    final_name = f'{instance.id}/{instance.user.username}/{ext}'
    return f'userImages/{final_name}/{instance.id}'


class UserInformation( models.Model ):
    user = models.OneToOneField( User, on_delete=models.CASCADE, verbose_name='کاربر' )
    age = models.IntegerField( default=0, verbose_name='سن کاربر' )
    image = models.ImageField( upload_to=upload_image_path, verbose_name='تصویر کاربر', default='default.jpg' )
    education = models.CharField( max_length=30, verbose_name='تحصیلات کاربر', default='کارشناسی' )
    date_added = jmodels.jDateTimeField( verbose_name='تاریخ ثبت نام کاربر', default=datetime.datetime.now(), null=True,
                                         blank=True )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'اطلاعات کاربر'
        verbose_name_plural = 'اطلاعات کاربران'
        ordering = ['-date_added']
