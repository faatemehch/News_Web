from django.urls import path
from .views import (PostListView,
                    PostDetailView,
                    PostSearchView,
                    PostByCategoryView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    like_or_dislike_post
                    )

urlpatterns = [
    path( 'news/', PostListView.as_view(), name='all_news' ),
    path( 'news/<int:pk>', PostDetailView.as_view(), name='post_detail' ),
    path( 'news/search', PostSearchView.as_view(), name='post_search' ),
    path( 'news/<category_title>', PostByCategoryView.as_view(), name='post_category' ),
    path( 'post/new/', PostCreateView.as_view(), name='post-create' ),
    path( 'post/update/<int:pk>', PostUpdateView.as_view(), name='post-update' ),
    path( 'post/delete/<int:pk>', PostDeleteView.as_view(), name='post-delete' ),
    path( 'news/<int:id>/<value>', like_or_dislike_post, name='post-like' ),
]
