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
    """
    API endpoint for creating new articles.

    Only authenticated users with the *journalist* role may create articles.
    The authenticated user is automatically assigned as the article author.
    """

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
    """
    API endpoint for updating an existing article.

    Permissions
    -----------
    - Editors may update any article.
    - Journalists may update only their own articles.
    """

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
    """
    API endpoint for deleting an article.

    Permissions
    -----------
    - Editors may delete any article.
    - Journalists may delete only their own articles.
    """

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
    """
    API endpoint for creating newsletters.

    Only authenticated journalists may create newsletters.
    The authenticated user becomes the newsletter author.
    """

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
    """
    API endpoint for updating newsletters.

    Permissions
    -----------
    - Editors may update any newsletter.
    - Journalists may update only newsletters they authored.
    """

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
    """
    API endpoint for deleting newsletters.

    Permissions
    -----------
    - Editors may delete any newsletter.
    - Journalists may delete only newsletters they authored.
    """

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
    """
    API endpoint for adding an article to a newsletter.

    Only the journalist who authored the newsletter may modify it.
    """

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
    """
    Subscribe the authenticated user to a publisher.
    """

    def post(self, request, pk):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("Authentication required.")

        publisher = get_object_or_404(Publisher, id=pk)
        user.subscriptions_publishers.add(publisher)
        return Response({"message": "Subscribed"}, status=status.HTTP_200_OK)


class UnsubscribePublisherView(generics.GenericAPIView):
    """
    Unsubscribe the authenticated user from a publisher.
    """

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
    """
    Subscribe the authenticated user to a journalist.
    """

    def post(self, request, pk):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("Authentication required.")

        journalist = get_object_or_404(User, id=pk, role=User.JOURNALIST)
        user.subscriptions_journalists.add(journalist)
        return Response({"message": "Subscribed"}, status=status.HTTP_200_OK)


class UnsubscribeJournalistView(generics.GenericAPIView):
    """
    Unsubscribe the authenticated user from a journalist.
    """

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
    """
    Return all articles from publishers and journalists the user follows.

    Requires authentication.
    """

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
    """
    Dummy endpoint used for testing article approval signals.

    Accepts POST requests and returns a success message.
    """

    def post(self, request):
        return Response({"message": "Signal received"}, status=status.HTTP_200_OK)
