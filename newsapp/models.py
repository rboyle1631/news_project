from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    READER = "reader"
    EDITOR = "editor"
    JOURNALIST = "journalist"

    ROLE_CHOICES = [
        (READER, "Reader"),
        (EDITOR, "Editor"),
        (JOURNALIST, "Journalist"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    subscriptions_publishers = models.ManyToManyField(
        Publisher,
        blank=True,
        related_name="subscribed_readers"
    )

    subscriptions_journalists = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="journalist_subscribers"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Assign user to a group based on role
        if self.role:
            group_name = self.role.capitalize()
            try:
                group = Group.objects.get(name=group_name)
                self.groups.set([group])
            except Group.DoesNotExist:
                pass

        # Journalists cannot have reader subscriptions
        if self.role == self.JOURNALIST:
            self.subscriptions_publishers.clear()
            self.subscriptions_journalists.clear()

    def __str__(self):
        return f"{self.username} ({self.role})"


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="articles"
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles"
    )

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="newsletters"
    )

    articles = models.ManyToManyField(
        Article,
        related_name="newsletters",
        blank=True
    )

    def __str__(self):
        return self.title
