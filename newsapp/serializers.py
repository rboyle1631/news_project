from rest_framework import serializers
from .models import Article, Newsletter, Publisher, User


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "title", "content", "publisher"]


class ArticleDetailSerializer(serializers.ModelSerializer):
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
