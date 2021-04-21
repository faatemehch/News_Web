from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class ContactUs( models.Model ):
    user = models.ForeignKey( User, on_delete=models.CASCADE, verbose_name='نام کاربری' )
    email = models.EmailField( verbose_name='ایمیل', max_length=150 , null=True, blank=True)
    title = models.CharField( max_length=200, verbose_name='عنوان پیام' )
    text = models.TextField( verbose_name='متن پیام' )
    is_read = models.BooleanField( default=False, verbose_name='خوانده شده/نشده' )

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'تماس کاربر'
        verbose_name_plural = 'تماس‌های کاربران'
