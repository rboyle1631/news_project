from rest_framework import serializers
from .models import Article, Newsletter, Publisher, User


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and listing basic Article data.

    This serializer is used for simple article representations,
    such as list views or lightweight API responses.
    """

    class Meta:
        model = Article
        fields = ["id", "title", "content", "publisher"]


class ArticleDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed Article views.

    Includes related fields such as author and publisher names,
    and exposes the article creation timestamp.
    """

    author = serializers.StringRelatedField()
    publisher = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "author",
            "publisher",
            "created_at",
        ]


class NewsletterSerializer(serializers.ModelSerializer):
    """
    Serializer for Newsletter objects.

    Provides read‑only access to the author ID and associated articles.
    Used for listing and retrieving newsletter data.
    """

    author = serializers.IntegerField(source="author.id", read_only=True)
    articles = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Newsletter
        fields = [
            "id",
            "title",
            "description",
            "author",
            "created_at",
            "articles",
        ]
        read_only_fields = ["author", "created_at", "articles"]
