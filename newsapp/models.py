from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class Publisher(models.Model):
    """
    Represents a news publisher that users can subscribe to.

    Attributes
    ----------
    name : str
        The name of the publisher.
    description : str
        Optional description or summary of the publisher.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Custom user model with role-based permissions and subscription logic.

    Roles
    -----
    reader : Can read approved articles and subscribe to publishers/journalists.
    editor : Can approve articles.
    journalist : Can write articles but cannot subscribe to others.

    Attributes
    ----------
    role : str
        The user's role within the system.
    subscriptions_publishers : ManyToManyField
        Publishers the user is subscribed to (readers only).
    subscriptions_journalists : ManyToManyField
        Journalists the user follows (readers only).
    """

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
        """
        Save the user and automatically assign them to the correct Django group.

        Ensures:
        - Users are added to a group matching their role.
        - Journalists cannot have subscriptions.
        """
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
    """
    Represents a news article written by a journalist.

    Attributes
    ----------
    title : str
        The title of the article.
    content : str
        The full text of the article.
    created_at : datetime
        When the article was created.
    approved : bool
        Whether the article has been approved by an editor.
    author : User
        The journalist who wrote the article.
    publisher : Publisher
        The publisher associated with the article.
    """

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
    """
    Represents a newsletter containing multiple articles.

    Attributes
    ----------
    title : str
        The title of the newsletter.
    description : str
        Optional summary or description.
    created_at : datetime
        When the newsletter was created.
    author : User
        The user who created the newsletter.
    articles : ManyToManyField
        Articles included in the newsletter.
    """

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
