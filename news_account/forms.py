from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.models import User
from django.core import validators

from news_account.models import UserInformation


class LoginForm( forms.Form ):
    user_name = forms.CharField( widget=forms.TextInput( attrs={
        'type': 'text'
    } ), label='نام کاربری:', validators=
    [validators.MaxLengthValidator( limit_value=20,
                                    message='تعداد کاراکتر‌های وارد شده از ۲۰ کاراکتر نمی‌تواند بیشتر باشد!' )
     ] )

    password = forms.CharField( widget=forms.PasswordInput( attrs={
        'type': 'password'
    } ), label='رمز عبور:' )

    captcha = CaptchaField()

    def clean_user_name(self):
        user_name = self.cleaned_data.get( 'user_name' )
        is_exist = User.objects.filter( username=user_name ).exists()
        if not is_exist:
            raise forms.ValidationError( 'کاربری با مشخضات وارد شده یافت نشد!' )
        return user_name


class RegisterForm( forms.Form ):
    user_name = forms.CharField( widget=forms.TextInput( attrs={
        'type': 'text'} ), label='نام کاربری:', validators=
    [validators.MaxLengthValidator( limit_value=20,
                                    message='تعداد کاراکتر‌های وارد شده از ۲۰ کاراکتر نمی‌تواند بیشتر باشد!' )
     ] )
    email = forms.CharField( widget=forms.EmailInput( attrs={
        'type': 'email'
    } ), label='ایمیل:',
        validators=
        [validators.MaxLengthValidator( limit_value=50,
                                        message='تعداد کاراکتر‌های وارد شده از ۵۰ کاراکتر نمی‌تواند بیشتر باشد!' )
         ] )
    password = forms.CharField( widget=forms.PasswordInput( attrs={
        'type': 'password'
    } ), label='رمز عبور:' )
    re_password = forms.CharField( widget=forms.PasswordInput( attrs={
        'type': 'password'
    } ), label='تکرار رمز عبور:' )

    def clean_user_name(self):
        user_name = self.cleaned_data.get( 'user_name' )
        qs = User.objects.filter( username=user_name ).exists()
        if qs:
            raise forms.ValidationError( 'لطفا نام کاربری دیگری وارد کنید!' )
        return user_name

    def clean_email(self):
        email = self.cleaned_data.get( 'email' )
        qs = User.objects.filter( email=email ).exists()
        if qs:
            raise forms.ValidationError( 'لطفاایمیل دیگری وارد کنید!' )
        return email

    def clean_re_password(self):
        password = self.cleaned_data.get( 'password' )
        re_password = self.cleaned_data.get( 're_password' )
        if password != re_password:
            raise forms.ValidationError( 'رمز عبور و تکرار آن باید باهم مطابقت داشته باشند!' )
        return re_password


class UserForm( forms.ModelForm ):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserInformationForm( forms.ModelForm ):
    class Meta:
        model = UserInformation
        fields = ['age', 'education', 'image']
