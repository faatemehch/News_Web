from .forms import LoginForm, RegisterForm, UserForm, UserInformationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import View, ListView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from news_blog_post.models import Post
from .models import UserInformation


class LoginView( View ):
    form_class = LoginForm
    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect( 'home' )
        login_from = self.form_class()
        context = {
            'title': 'ورود به سایت',
            'login_from': login_from
        }
        return render( request, self.template_name, context )

    def post(self, request, *args, **kwargs):
        login_form = self.form_class( request.POST or None )
        if login_form.is_valid():
            user_name = login_form.cleaned_data.get( 'user_name' )
            password = login_form.cleaned_data.get( 'password' )
            user = authenticate( username=user_name, password=password )
            if user is not None:
                login( request, user )
                return redirect( 'home' )
            login_form.add_error( 'user_name', '  مشخصات وارد شده نادرست می‌باشد!' )
        context = {
            'title': 'ورود به سایت',
            'login_from': login_form
        }
        return render( request, self.template_name, context )


class RegisterView( View ):
    form_class = RegisterForm
    template_name = 'account/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect( 'home' )
        register_form = self.form_class()
        context = {
            'title': 'ثبت نام در سایت',
            'register_form': register_form
        }
        return render( request, self.template_name, context )

    def post(self, request):
        register_form = self.form_class( request.POST or None )
        if register_form.is_valid():
            user_name = register_form.cleaned_data.get( 'user_name' )
            email = register_form.cleaned_data.get( 'email' )
            password = register_form.cleaned_data.get( 'password' )
            user: User = User.objects.create_user( username=user_name, email=email, password=password )
            UserInformation.objects.create( user=user )
            print( user )
            if user is not None:
                return redirect( 'login' )
        context = {
            'title': 'ثبت نام در سایت',
            'register_form': register_form
        }
        return render( request, self.template_name, context )


class Logout( View, LoginRequiredMixin ):

    def get(self, request, *args, **kwargs):
        logout( request )
        return redirect( 'login' )


class UserInformationView( ListView ):
    model = Post
    template_name = 'account/user_information.html'
    paginate_by = 6

    def get_context_data(self, *args, **kwargs):
        user_info = UserInformation.objects.filter( user_id=self.kwargs.get( 'id' ) ).first()
        list_object = Post.objects.filter( author_id=self.kwargs.get( 'id' ) ).all()
        page = self.request.GET.get( 'page', 1 )
        paginator = Paginator( list_object, 6 )
        try:
            sets = paginator.page( page )
        except PageNotAnInteger:
            sets = paginator.page( 1 )
        except EmptyPage:
            sets = paginator.page( paginator.num_pages )
        context = super().get_context_data( **kwargs )
        context['user_info'] = user_info
        context['title'] = 'اطلاعات کاربری'
        context['sets'] = sets

        return context

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter( author_id=self.kwargs.get( 'id' ) ).all().order_by( '-date_added' )


class UpdateUserInformationView( UpdateView, LoginRequiredMixin ):
    model = User
    template_name = 'account/update_user_info.html'
    form_class = UserForm
    form_class_user_info = UserInformationForm

    def get(self, request, *args, **kwargs):
        context = {'user_form_1': self.form_class( instance=request.user ),

                   'user_form_2': self.form_class_user_info( instance=request.user.userinformation ),
                   'title': 'ویرایش اطلاعات کاربری'
                   }
        return render( self.request, self.template_name, context )

    def post(self, request, *args, **kwargs):
        user_form_1 = self.form_class( request.POST,
                                       instance=request.user )
        user_form_2 = self.form_class_user_info( request.POST,
                                                 request.FILES,
                                                 instance=request.user.userinformation )
        if user_form_1.is_valid() and user_form_2.is_valid():
            user_form_1.save()
            user_form_2.save()
            return redirect( 'home' )
        context = {
            'title': 'ویرایش اطلاعات کاربری',
            'user_form_1': user_form_1,
            'user_form_2': user_form_2
        }
        return render( self.request, self.template_name, context )



