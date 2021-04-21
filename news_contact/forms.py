from django import forms
from django.core import validators
from django.contrib.auth.models import User


class ContactForm( forms.Form ):
    user_name = forms.CharField( widget=forms.TextInput(
        attrs={'type': 'text'} ), label='نام کاربری', validators=[
        validators.MaxLengthValidator( 150, 'نام کاربری شما نمی‌تواند بیش‌ از ۱۵۰ کاراکتر باشد!' )
    ]
    )
    email = forms.EmailField( widget=forms.EmailInput(
        attrs={'type': 'email'} ), label='ایمیل', validators=[
        validators.MaxLengthValidator( 150, 'ایمیل شما نمی‌تواند بیش‌ از ۱۵۰ کاراکتر باشد!' )
    ]
    )
    title = forms.CharField( widget=forms.TextInput( attrs={'type': 'text'} ), label='عنوان پیام' )

    text = forms.CharField( widget=forms.Textarea( attrs={'rows': '3'} ), label='متن پیام'
                            )

    def clean_email(self):
        user_name = self.cleaned_data.get( 'user_name' )
        email = self.cleaned_data.get( 'email' )
        qs = User.objects.filter( username=user_name, email=email ).exists()
        if not qs:
            raise forms.ValidationError( 'نام کاربری و ایمیل وارد شده صحیح نیست!' )
        return email
