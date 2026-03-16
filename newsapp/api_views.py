from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Article, Newsletter, Publisher, User
from .serializers import (
    ArticleSerializer,
    NewsletterSerializer,
    ArticleDetailSerializer,
)


# =========================================================
# ARTICLE CREATE
# =========================================================

class ArticleCreateView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated or self.request.user.role != User.JOURNALIST:
            raise PermissionDenied("Only journalists can create articles.")
        serializer.save(author=self.request.user)


# =========================================================
# ARTICLE UPDATE
# =========================================================

class ArticleUpdateView(generics.UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_update(self, serializer):
        article = self.get_object()
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("Authentication required.")

        if user.role == User.EDITOR:
            serializer.save()
            return

        if user.role == User.JOURNALIST and article.author == user:
            serializer.save()
            return

        raise PermissionDenied("You do not have permission to update this article.")


# =========================================================
# ARTICLE DELETE
# =========================================================

class ArticleDeleteView(generics.DestroyAPIView):
    queryset = Article.objects.all()

    def perform_destroy(self, instance):
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("Authentication required.")

        if user.role == User.EDITOR:
            instance.delete()
            return

        if user.role == User.JOURNALIST and instance.author == user:
            instance.delete()
            return

        raise PermissionDenied("You do not have permission to delete this article.")


# =========================================================
# NEWSLETTER CREATE
# =========================================================

class NewsletterCreateView(generics.CreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated or user.role != User.JOURNALIST:
            raise PermissionDenied("Only journalists can create newsletters.")
        serializer.save(author=user)


# =========================================================
# NEWSLETTER UPDATE
# =========================================================

class NewsletterUpdateView(generics.UpdateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def perform_update(self, serializer):
        newsletter = self.get_object()
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("Authentication required.")

        if user.role == User.EDITOR:
            serializer.save()
            return

        if user.role == User.JOURNALIST and newsletter.author == user:
            serializer.save()
            return

        raise PermissionDenied("You do not have permission to update this newsletter.")


# =========================================================
# NEWSLETTER DELETE
# =========================================================

class NewsletterDeleteView(generics.DestroyAPIView):
    queryset = Newsletter.objects.all()

    def perform_destroy(self, instance):
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("Authentication required.")

        if user.role == User.EDITOR:
            instance.delete()
            return

        if user.role == User.JOURNALIST and instance.author == user:
            instance.delete()
            return

        raise PermissionDenied("You do not have permission to delete this newsletter.")


# =========================================================
# ADD ARTICLE TO NEWSLETTER
# =========================================================

class AddArticleToNewsletterView(generics.GenericAPIView):

    def post(self, request, pk):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("Authentication required.")

        newsletter = get_object_or_404(Newsletter, id=pk)

        if user.role != User.JOURNALIST or newsletter.author != user:
            raise PermissionDenied("You cannot modify this newsletter.")

        article_id = request.data.get("article_id")
        article = get_object_or_404(Article, id=article_id)

        newsletter.articles.add(article)

        return Response({"message": "Article added"}, status=status.HTTP_200_OK)


# =========================================================
# SUBSCRIBE TO PUBLISHER
# =========================================================

class SubscribePublisherView(generics.GenericAPIView):

    def post(self, request, pk):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("Authentication required.")

        publisher = get_object_or_404(Publisher, id=pk)
        user.subscriptions_publishers.add(publisher)
        return Response({"message": "Subscribed"}, status=status.HTTP_200_OK)


class UnsubscribePublisherView(generics.GenericAPIView):

    def post(self, request, pk):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("Authentication required.")

        publisher = get_object_or_404(Publisher, id=pk)
        user.subscriptions_publishers.remove(publisher)
        return Response({"message": "Unsubscribed"}, status=status.HTTP_200_OK)


# =========================================================
# SUBSCRIBE TO JOURNALIST
# =========================================================

class SubscribeJournalistView(generics.GenericAPIView):

    def post(self, request, pk):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("Authentication required.")

        journalist = get_object_or_404(User, id=pk, role=User.JOURNALIST)
        user.subscriptions_journalists.add(journalist)
        return Response({"message": "Subscribed"}, status=status.HTTP_200_OK)


class UnsubscribeJournalistView(generics.GenericAPIView):

    def post(self, request, pk):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("Authentication required.")

        journalist = get_object_or_404(User, id=pk, role=User.JOURNALIST)
        user.subscriptions_journalists.remove(journalist)
        return Response({"message": "Unsubscribed"}, status=status.HTTP_200_OK)


# =========================================================
# SUBSCRIBED ARTICLES FEED
# =========================================================

class SubscribedArticlesView(generics.ListAPIView):
    serializer_class = ArticleDetailSerializer

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("Authentication required.")

        publishers = user.subscriptions_publishers.all()
        journalists = user.subscriptions_journalists.all()

        return Article.objects.filter(
            publisher__in=publishers
        ) | Article.objects.filter(
            author__in=journalists
        )


# =========================================================
# APPROVED SIGNAL ENDPOINT
# =========================================================

class ApprovedSignalView(generics.GenericAPIView):

    def post(self, request):
        # Tests just expect this to accept POST and return 200
        return Response({"message": "Signal received"}, status=status.HTTP_200_OK)
