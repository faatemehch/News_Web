from django import forms
from django.core import validators
from .views import PostImage


class CommentForm( forms.Form ):
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'text'} ),
        label='نام و نام خانوادگی',
        validators=[validators.MaxLengthValidator( 120, 'نام و نام خانوادگی شما نمی‌تواند بیش از ۱۵۰ کاراکتر باشد' )] )

    text = forms.CharField(
        widget=forms.Textarea( attrs={'rows': 3} ), label='متن نظر' )


class ImageForm( forms.ModelForm ):
    class Meta:
        model = PostImage
        fields = ['image_1', 'image_2']
