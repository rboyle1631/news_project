from django.urls import path
from .views import approve_article, article_detail

urlpatterns = [
    path('articles/<int:article_id>/', article_detail, name='article_detail'),
    path('articles/<int:article_id>/approve/', approve_article, name='approve_article'),
]
