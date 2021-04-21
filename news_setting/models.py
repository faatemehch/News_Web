from django.db import models
import os


def get_file_name_ext(file_path):
    base_name = os.path.basename( file_path )
    name, ext = os.path.splitext( base_name )
    return name, ext


def upload_image_path(instance, fileName):
    name, ext = get_file_name_ext( fileName )
    final_name = f'{instance.id}/{ext}'
    return f'settingImages/{final_name}'


class Setting( models.Model ):
    logo_img = models.ImageField( verbose_name='تصویر لوگو', upload_to=upload_image_path )
    larger_image = models.ImageField( verbose_name='تصویر بزرگ', upload_to=upload_image_path )
    little_image_first = models.ImageField( verbose_name='تصویر کوچک ۱', upload_to=upload_image_path )
    little_image_second = models.ImageField( verbose_name='تصویر کوچک ۲', upload_to=upload_image_path )

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'

    def __str__(self):
        return 'تنظیمات سایت'


class AboutUs( models.Model ):
    about_img = models.ImageField( verbose_name='تصویر درباره ما', upload_to=upload_image_path )
    about_text = models.TextField( verbose_name='متن درباره ما' )

    class Meta:
        verbose_name = 'درباره ما'
        verbose_name_plural = 'درباره ما'

    def __str__(self):
        return 'درباره ما'
