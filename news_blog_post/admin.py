from django.contrib import admin
from .models import Post, PostImage, PostCategory, Comment_Post, VisitedIpPost


# Register your models here.
class PostAdmin( admin.ModelAdmin ):
    list_display = ['__str__', 'date_added']


class CommentAdmin( admin.ModelAdmin ):
    list_display = ['__str__', 'is_read', 'date_added']


admin.site.register( Post, PostAdmin )
admin.site.register( PostImage )
admin.site.register( PostCategory )
admin.site.register( Comment_Post, CommentAdmin )
admin.site.register( VisitedIpPost )
