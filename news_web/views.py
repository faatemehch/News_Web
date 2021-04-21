from django.shortcuts import render
from news_setting.models import Setting
from news_blog_post.models import PostCategory
from news_blog_post.models import Post


def get_cat_count():
    posts = Post.objects.all()
    categories = PostCategory.objects.all()
    categories_count = {}
    for category in categories:
        for post in posts:
            if category.title == post.categories_post.title:
                if category.title in categories_count:
                    categories_count[f'{category.title}'] += 1
                else:
                    categories_count[f'{category.title}'] = 1
    return categories_count


# home page view
def home(request):
    context = {
        'title': 'صفحه اصلی',
        'setting': Setting.objects.last(),
        'most_like': Post.objects.all().order_by( '-like_count' )[:4],
        'new_posts': Post.objects.all().order_by( '-date_added' )[:4],
        'count_post_categories': get_cat_count()
    }
    print( get_cat_count() )
    return render( request, 'home.html', context )


# code behind
def header(request):
    context = {'categories': PostCategory.objects.all()}
    return render( request, 'shared/header.html', context )


def footer(request):
    context = {

    }
    return render( request, 'shared/footer.html', context )
