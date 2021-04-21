import jdatetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django_jalali.db import models as jmodels
import os


class PostManager( models.Manager ):
    def get_post_by_id(self, post_id):
        return self.get_queryset().filter( id=post_id ).first()

    def search(self, query):
        lookup = Q( title__icontains=query ) | Q( content__icontains=query )
        return self.get_queryset().filter( lookup ).distinct()

    def get_post_by_category(self, category):
        return self.get_queryset().filter( categories_post__title__contains=category ).all()


def get_file_name_ext(file_path):
    base_name = os.path.basename( file_path )
    name, ext = os.path.splitext( base_name )
    return name, ext


def upload_image_path(instance, fileName):
    name, ext = get_file_name_ext( fileName )
    final_name = f'{instance.id}/{ext}'
    return f'postImages/{instance.id}/{final_name}'


class Post( models.Model ):
    title = models.CharField( max_length=200, verbose_name='عنوان خبر' )
    author = models.ForeignKey( User, on_delete=models.CASCADE, verbose_name='منتشر کننده خبر' )
    content = models.TextField( verbose_name='متن خبر' )
    date_added = jmodels.jDateTimeField( verbose_name='تاریخ ایجاد خبر', default=jdatetime.datetime.now() )
    image = models.OneToOneField( 'PostImage', verbose_name='تصویر خبر', null=True, blank=True,
                                  on_delete=models.CASCADE )
    categories_post = models.ForeignKey( 'PostCategory', null=True, blank=True, verbose_name='دسته بندی خبر',
                                         on_delete=models.CASCADE )

    like_count = models.IntegerField( verbose_name='تعداد پسندها', default=0 )
    dislike_count = models.IntegerField( verbose_name='تعداد نپسندها', default=0 )

    objects = PostManager()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['-date_added']
        verbose_name = 'خبر جدید'
        verbose_name_plural = 'خبرها'

    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostImage( models.Model ):
    image_1 = models.ImageField( upload_to=upload_image_path, verbose_name='تصویر خبر ۱' )
    image_2 = models.ImageField( upload_to=upload_image_path, verbose_name='تصویر خبر ۲' )

    def __str__(self):
        return 'تصاویر خبر'

    class Meta:
        verbose_name = 'تصویر خبر'
        verbose_name_plural = 'تصاویر خبرها'


class PostCategory( models.Model ):
    title = models.CharField( max_length=200, verbose_name='عنوان دسته‌بندی' )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته‌بندی خبر'
        verbose_name_plural = 'دسته‌بندی خبرها'


class Comment_Post( models.Model ):
    post = models.ForeignKey( Post, on_delete=models.CASCADE, verbose_name='خبر مربوطه' )
    owner = models.ForeignKey( User, on_delete=models.CASCADE, verbose_name='نام کاربری' )
    full_name = models.CharField( max_length=150, verbose_name='نام و نام‌خانوادگی' )
    text = models.TextField( verbose_name='متن نظر' )
    date_added = jmodels.jDateTimeField( verbose_name='تاریخ ایجاد نظر' )
    is_read = models.BooleanField( default=False, verbose_name='خوانده شده/نشده' )

    def __str__(self):
        return f'{self.post}'

    class Meta:
        verbose_name = 'نظر کاربر'
        verbose_name_plural = 'نظرات کاربران'
        ordering = ['-date_added']


class VisitedIpPost( models.Model ):
    post = models.ForeignKey( Post, on_delete=models.CASCADE, verbose_name='خبر مربوطه' )
    user_ip = models.TextField( verbose_name='آدرس‌ها' )
    value = models.BooleanField(verbose_name='نظر ثبت شده', default=False)

    def __str__(self):
        return self.user_ip

    class Meta:
        verbose_name = 'آدرس ip کاربر'
        verbose_name_plural = 'آدرس ip کاربر'
