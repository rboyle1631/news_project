from django.urls import path
from .api_views import (
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
    NewsletterCreateView,
    NewsletterUpdateView,
    NewsletterDeleteView,
    AddArticleToNewsletterView,
    SubscribePublisherView,
    UnsubscribePublisherView,
    SubscribeJournalistView,
    UnsubscribeJournalistView,
    SubscribedArticlesView,
    ApprovedSignalView,
)

urlpatterns = [
    # Articles
    path('articles/create/', ArticleCreateView.as_view()),
    path('articles/<int:pk>/update/', ArticleUpdateView.as_view()),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view()),

    # Newsletters
    path('newsletters/create/', NewsletterCreateView.as_view()),
    path('newsletters/<int:pk>/update/', NewsletterUpdateView.as_view()),
    path('newsletters/<int:pk>/delete/', NewsletterDeleteView.as_view()),
    path('newsletters/<int:pk>/add-article/', AddArticleToNewsletterView.as_view()),

    # Subscriptions
    path('publishers/<int:pk>/subscribe/', SubscribePublisherView.as_view()),
    path('publishers/<int:pk>/unsubscribe/', UnsubscribePublisherView.as_view()),
    path('journalists/<int:pk>/subscribe/', SubscribeJournalistView.as_view()),
    path('journalists/<int:pk>/unsubscribe/', UnsubscribeJournalistView.as_view()),

    # Subscribed feed
    path('articles/subscribed/', SubscribedArticlesView.as_view()),

    # Approved signal
    path('approved/', ApprovedSignalView.as_view()),
]
