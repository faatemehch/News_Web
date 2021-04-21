import jdatetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.views.generic.list import MultipleObjectMixin
from .models import Post, PostImage, Comment_Post, VisitedIpPost
from .forms import CommentForm, ImageForm


class PostListView( ListView ):
    template_name = 'news_blog_post/post_listView.html'
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs )

        list_object = Post.objects.all()
        page = self.request.GET.get( 'page', 1 )
        paginator = Paginator( list_object, 6 )
        try:
            sets = paginator.page( page )
        except PageNotAnInteger:
            sets = paginator.page( 1 )
        except EmptyPage:
            sets = paginator.page( paginator.num_pages )
        context['sets'] = sets
        context['inner_title'] = 'مشاهده تمامی خبرها'
        context['title'] = 'خبرها'

        return context


class PostDetailView( DetailView, MultipleObjectMixin ):
    model = Post
    form_class = CommentForm
    template_name = 'news_blog_post/post_detailView.html'
    paginate_by = 3

    def post(self, request, *args, **kwargs):
        comment_form = self.form_class( request.POST )
        if comment_form.is_valid():
            full_name = comment_form.cleaned_data.get( 'full_name' )
            text = comment_form.cleaned_data.get( 'text' )
            Comment_Post.objects.create( post_id=self.kwargs.get( 'pk' ),
                                         owner_id=self.request.user.id,
                                         full_name=full_name,
                                         text=text,
                                         date_added=jdatetime.datetime.now() )
            return HttpResponseRedirect( request.META.get( 'HTTP_REFERER' ) )

    def get_context_data(self, *args, **kwargs):
        post = Post.objects.get_post_by_id( self.kwargs.get( 'pk' ) )
        comments = Comment_Post.objects.filter( post_id=self.kwargs.get( 'pk' ) ).all()
        context = super( PostDetailView, self ).get_context_data( object_list=comments, **kwargs )
        page = self.request.GET.get( 'page' )
        paginator = Paginator( comments, 3 )
        try:
            page_obj = paginator.page( page )
        except PageNotAnInteger:
            page_obj = paginator.page( 1 )
        except EmptyPage:
            page_obj = paginator.page( paginator.num_pages )
        context['post_detail_img'] = PostImage.objects.filter( post=post )
        context['title'] = 'مشاهده جزئیات خبر'
        context['comments'] = comments
        context['sets'] = page_obj
        context['comment_form'] = self.form_class()
        return context


class PostSearchView( ListView ):
    template_name = 'news_blog_post/post_listView.html'
    paginate_by = 9

    def get_queryset(self):
        return Post.objects.search( query=self.request.GET.get( 'q' ) )

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs )

        list_object = Post.objects.search( query=self.request.GET.get( 'q' ) )
        page = self.request.GET.get( 'page', 1 )
        paginator = Paginator( list_object, 6 )
        try:
            sets = paginator.page( page )
        except PageNotAnInteger:
            sets = paginator.page( 1 )
        except EmptyPage:
            sets = paginator.page( paginator.num_pages )

        context['title'] = 'نتایج جستجو'
        context['sets'] = sets
        context['inner_title'] = 'مشاهده نتایج جستجو'
        return context


class PostByCategoryView( ListView ):
    template_name = 'news_blog_post/post_listView.html'
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.get_post_by_category( category=self.kwargs.get( 'category_title' ) )

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs )
        list_object = Post.objects.get_post_by_category( category=self.kwargs.get( 'category_title' ) )
        page = self.request.GET.get( 'page', 1 )
        paginator = Paginator( list_object, 6 )
        try:
            sets = paginator.page( page )
        except PageNotAnInteger:
            sets = paginator.page( 1 )
        except EmptyPage:
            sets = paginator.page( paginator.num_pages )

        context['title'] = 'نتایج جستجو'
        context['sets'] = sets
        context['inner_title'] = f'مشاهده خبرهای {self.kwargs.get( "category_title" )} '
        return context


class PostCreateView( LoginRequiredMixin, CreateView ):
    model = Post
    fields = ['title', 'content', 'categories_post']

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs )
        context['image_form'] = ImageForm()
        context['title'] = 'افزودن خبر'
        return context

    def form_valid(self, form):
        image_form = ImageForm( self.request.POST, self.request.FILES )
        if image_form.is_valid():
            images_1 = image_form.cleaned_data.get( 'image_1' )
            images_2 = image_form.cleaned_data.get( 'image_2' )
            image_post = PostImage.objects.create( image_1=images_1, image_2=images_2 )
            form.instance.image = image_post
            form.instance.date_added = jdatetime.datetime.now()
            form.instance.author = self.request.user
            return super().form_valid( form )
        return HttpResponseRedirect( self.request.path_info )


# just owner can delete an edit the post
class PostUpdateView( LoginRequiredMixin, UserPassesTestMixin, UpdateView ):
    model = Post
    fields = ['title', 'content', 'categories_post', 'image']

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs )
        context['image_form'] = ImageForm()
        context['title'] = 'ویرایش خبر'
        return context

    def form_valid(self, form):
        image_form = ImageForm( self.request.POST, self.request.FILES )
        if image_form.is_valid():
            images_1 = image_form.cleaned_data.get( 'image_1' )
            images_2 = image_form.cleaned_data.get( 'image_2' )
            image_post = PostImage.objects.create( image_1=images_1, image_2=images_2 )
            image_post.save()
            form.instance.image = image_post
            form.instance.date_added = jdatetime.datetime.now()
            return super().form_valid( form )
        return HttpResponseRedirect( self.request.path_info )

    def test_func(self):
        post = self.get_object()  # get the consider post
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView( LoginRequiredMixin, UserPassesTestMixin, DeleteView ):
    model = Post

    def get_success_url(self):
        return self.request.GET.get( 'next', reverse( 'home' ) )

    def test_func(self):
        post = self.get_object()  # get the consider post
        if self.request.user == post.author:
            return True
        return False


def like_or_dislike_post(request, *args, **kwargs):
    address = request.META.get( 'HTTP_X_FORWARDED_FOR' )
    get_value = kwargs.get( 'value' )
    post_id = kwargs.get( 'id' )
    if address:
        ip = address.split( ',' )[-1].strip()
    else:
        ip = request.META.get( 'REMOTE_ADDR' )
    visited_ip_post = VisitedIpPost.objects.filter( post_id=post_id, user_ip=ip ).all()
    post = Post.objects.filter( id=post_id ).first()
    if len( visited_ip_post ) == 0:
        visited_ip_post = VisitedIpPost.objects.create( post=post, user_ip=ip )
        if get_value == 'True':
            visited_ip_post.value = True
            visited_ip_post.save()
            post.like_count += 1
            post.dislike_count -= 1
            post.save()
        else:
            visited_ip_post.value = False
            visited_ip_post.save()
            post.dislike_count += 1
            post.like_count -= 1
            post.save()
    else:
        if get_value == 'True' and not visited_ip_post[0].value:
            visited_ip_post[0].value = True
            visited_ip_post[0].save()
            post.like_count += 1
            post.dislike_count -= 1
            post.save()
        elif get_value == 'False' and visited_ip_post[0].value is True:
            visited_ip_post[0].value = False
            visited_ip_post[0].save()
            post.like_count -= 1
            post.dislike_count += 1
            post.save()
    return HttpResponseRedirect( reverse( 'post_detail', args=[int( post_id )] ) )
