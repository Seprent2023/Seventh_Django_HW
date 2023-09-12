from django.urls import path

from .views import (
    PostList, PostDetail, SearchResults, NewsCreate, ArticlesCreate, NewsUpdate, ArticlesUpdate, NewsDelete,
    ArticlesDelete, NewsList, ArticlesList, NewsDetail, ArticlesDetail, upgrade_user,
)

urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', SearchResults.as_view(), name='search'),
    path('upgrade/', upgrade_user, name='account_upgrade'),
    path('news/', NewsList.as_view(), name='news'),
    path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/', ArticlesList.as_view(), name='articles'),
    path('articles/<int:pk>', ArticlesDetail.as_view(), name='articles_detail'),
    path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', ArticlesUpdate.as_view(), name='articles_update'),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
    # path('', IndexView.as_view()),
]
