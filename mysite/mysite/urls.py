"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views

from blog.views import Blog_title
from account.views import Register
from article1.views import ArticleColumnView, RenameArticleColumnView, \
    DelArticleColumnView, ArticlePostView, ArticleListView, ArticleDetailView, \
    DelArticleView, ReditArticleFormView, ArticleTitleListView, LikeArticleView, \
    CommentFormView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', Blog_title.as_view(), name='blog_title'),
    # account
    # path('account/', UserLogin.as_view(), name='user_login'),
    path('account/', auth_views.LoginView.as_view(
        template_name='account/login.html'
    ), name='user_login'),
    path('account/logout', auth_views.LogoutView.as_view(
        template_name='account/logout.html'
    ), name='user_logout'),
    path('account/register/', Register.as_view(), name='user_register'),
    # article
    path('article/', ArticleColumnView.as_view(), name='article_column'),
    path('article/rename_article_column', RenameArticleColumnView.as_view(), name='rename_article_column'),
    path('article/del_article_column', DelArticleColumnView.as_view(), name='del_article_column'),
    path('article/article_post', ArticlePostView.as_view(), name='article_post'),
    path('article/article_list', ArticleListView.as_view(), name='article_list'),
    path(r'article/article-detail/(?P<id>\d+)/(?P<slug>[-\w]+/)$',
            ArticleDetailView.as_view(), name='article_detail'),
    path('article/del-article', DelArticleView.as_view(), name="del_article"),
    path(r'article/redit_article/(?P<article_id>\d+)/', ReditArticleFormView.as_view(), name='redit_article'),
    path('article/article_titles', ArticleTitleListView.as_view(), name='article_titles'),
    path('article/article_titles/<username>', ArticleTitleListView.as_view(), name='author_articles'),
    path('article/like_article', LikeArticleView.as_view(), name='like_article'),
    path(r'article/(?P<id>\d+)/(?P<slug>[-\w]+/)/comment/$',
         CommentFormView.as_view(), name='comments'),
    # re_path(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('', include('social_django.urls', namespace='social'))
]
