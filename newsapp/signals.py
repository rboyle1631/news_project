from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import requests
from .models import Article

@receiver(post_save, sender=Article)
def handle_article_approval(sender, instance, created, **kwargs):
    # Only act when an existing article is approved
    if created:
        return

    if instance.approved:
        # 1. Email subscribers
        subscribers = []

        if instance.publisher:
            subscribers = instance.publisher.subscribed_readers.all()
        else:
            subscribers = instance.author.journalist_subscribers.all()

        emails = [user.email for user in subscribers if user.email]

        if emails:
            send_mail(
                subject=f"New Approved Article: {instance.title}",
                message=instance.content[:200],
                from_email="no-reply@newsapp.com",
                recipient_list=emails,
                fail_silently=True,
            )

        # 2. POST to your own API endpoint
        try:
            requests.post(
                "http://127.0.0.1:8000/api/approved/",
                json={"article_id": instance.id, "title": instance.title},
                timeout=3
            )
        except Exception:
            pass
