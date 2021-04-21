"""news_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from news_web import settings
from django.conf.urls.static import static
from .views import home

urlpatterns = [
    path( 'admin/', admin.site.urls ),
    path( '', home, name='home' ),
    path( 'captcha/', include( 'captcha.urls' ) ),
    path( '', include( 'news_account.urls' ) ),
    path( '', include( 'forgot_password.urls' ) ),
    path( '', include( 'news_blog_post.urls' ) ),
    path( '', include( 'news_contact.urls' ) ),
    path( '', include( 'news_setting.urls' ) ),
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static( settings.STATIC_URL, document_root=settings.STATIC_ROOT )
    urlpatterns = urlpatterns + static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
