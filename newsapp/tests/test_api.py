from rest_framework.test import APITestCase
from rest_framework import status
from newsapp.models import User, Publisher, Article, Newsletter


class BaseAPITest(APITestCase):

    def setUp(self):
        # Create users
        self.reader = User.objects.create_user(
            username="reader", password="pass123", role=User.READER
        )
        self.journalist = User.objects.create_user(
            username="journalist", password="pass123", role=User.JOURNALIST
        )
        self.journalist2 = User.objects.create_user(
            username="journalist2", password="pass123", role=User.JOURNALIST
        )
        self.editor = User.objects.create_user(
            username="editor", password="pass123", role=User.EDITOR
        )

        # Create publisher
        self.publisher = Publisher.objects.create(name="Tech Daily")
        self.publisher2 = Publisher.objects.create(name="Sports Hub")

    def get_token(self, username, password="pass123"):
        response = self.client.post("/api/token/", {
            "username": username,
            "password": password
        })
        return response.data["access"]


# =========================================================
# ARTICLE TESTS
# =========================================================

class ArticleAPITest(BaseAPITest):

    # CREATE
    def test_journalist_can_create_article(self):
        token = self.get_token("journalist")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post("/api/articles/create/", {
            "title": "New Article",
            "content": "Content here",
            "publisher": self.publisher.id
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.first().author, self.journalist)

    def test_reader_cannot_create_article(self):
        token = self.get_token("reader")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post("/api/articles/create/", {
            "title": "Not Allowed",
            "content": "Readers cannot create",
            "publisher": self.publisher.id
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.count(), 0)

    # UPDATE
    def test_editor_can_update_any_article(self):
        token = self.get_token("journalist")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        create_response = self.client.post("/api/articles/create/", {
            "title": "Original Title",
            "content": "Original content",
            "publisher": self.publisher.id
        })

        article_id = create_response.data["id"]

        editor_token = self.get_token("editor")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {editor_token}")

        update_response = self.client.put(f"/api/articles/{article_id}/update/", {
            "title": "Updated by Editor",
            "content": "Editor changed this",
            "publisher": self.publisher.id
        })

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

    def test_journalist_can_update_only_their_own_article(self):
        token1 = self.get_token("journalist")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token1}")

        create_response = self.client.post("/api/articles/create/", {
            "title": "J1 Article",
            "content": "By journalist 1",
            "publisher": self.publisher.id
        })

        article_id = create_response.data["id"]

        token2 = self.get_token("journalist2")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token2}")

        update_response = self.client.put(f"/api/articles/{article_id}/update/", {
            "title": "Hacked by J2",
            "content": "Should not be allowed",
            "publisher": self.publisher.id
        })

        self.assertEqual(update_response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token1}")

        update_response2 = self.client.put(f"/api/articles/{article_id}/update/", {
            "title": "Updated by J1",
            "content": "Correct update",
            "publisher": self.publisher.id
        })

        self.assertEqual(update_response2.status_code, status.HTTP_200_OK)

    # DELETE
    def test_editor_can_delete_any_article(self):
        token = self.get_token("journalist")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        create_response = self.client.post("/api/articles/create/", {
            "title": "Delete Me",
            "content": "To be deleted",
            "publisher": self.publisher.id
        })

        article_id = create_response.data["id"]

        editor_token = self.get_token("editor")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {editor_token}")

        delete_response = self.client.delete(f"/api/articles/{article_id}/delete/")
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 0)

    def test_journalist_can_delete_only_their_own_article(self):
        token1 = self.get_token("journalist")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token1}")

        create_response = self.client.post("/api/articles/create/", {
            "title": "J1 Article",
            "content": "Owned by journalist 1",
            "publisher": self.publisher.id
        })

        article_id = create_response.data["id"]

        token2 = self.get_token("journalist2")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token2}")

        delete_response = self.client.delete(f"/api/articles/{article_id}/delete/")
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.count(), 1)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token1}")

        delete_response2 = self.client.delete(f"/api/articles/{article_id}/delete/")
        self.assertEqual(delete_response2.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 0)

    def test_reader_cannot_delete_article(self):
        token_j = self.get_token("journalist")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_j}")

        create_response = self.client.post("/api/articles/create/", {
            "title": "Protected Article",
            "content": "Readers cannot delete",
            "publisher": self.publisher.id
        })

        article_id = create_response.data["id"]

        token_r = self.get_token("reader")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_r}")

        delete_response = self.client.delete(f"/api/articles/{article_id}/delete/")
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.count(), 1)


# =========================================================
# NEWSLETTER TESTS
# =========================================================

class NewsletterAPITest(BaseAPITest):

    def test_journalist_can_create_newsletter(self):
        token = self.get_token("journalist")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post("/api/newsletters/create/", {
            "title": "Tech Weekly",
            "description": "Latest tech news"
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"], self.journalist.id)

    def test_reader_cannot_create_newsletter(self):
        token = self.get_token("reader")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post("/api/newsletters/create/", {
            "title": "Not Allowed",
            "description": "Readers cannot create newsletters"
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_update_any_newsletter(self):
        token_j = self.get_token("journalist")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_j}")

        create_response = self.client.post("/api/newsletters/create/", {
            "title": "Original",
            "description": "Original description"
        })

        newsletter_id = create_response.data["id"]

        token_e = self.get_token("editor")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_e}")

        update_response = self.client.put(f"/api/newsletters/{newsletter_id}/update/", {
            "title": "Updated by Editor",
            "description": "Editor changed this"
        })

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

    def test_journalist_can_update_only_their_own_newsletter(self):
        token1 = self.get_token("journalist")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token1}")

        create_response = self.client.post("/api/newsletters/create/", {
            "title": "J1 Newsletter",
            "description": "Owned by J1"
        })

        newsletter_id = create_response.data["id"]

        token2 = self.get_token("journalist2")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token2}")

        update_response = self.client.put(f"/api/newsletters/{newsletter_id}/update/", {
            "title": "Hacked by J2",
            "description": "Should not be allowed"
        })

        self.assertEqual(update_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_delete_any_newsletter(self):
        token_j = self.get_token("journalist")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_j}")

        create_response = self.client.post("/api/newsletters/create/", {
            "title": "Delete Me",
            "description": "To be deleted"
        })

        newsletter_id = create_response.data["id"]

        token_e = self.get_token("editor")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_e}")

        delete_response = self.client.delete(f"/api/newsletters/{newsletter_id}/delete/")
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_journalist_can_delete_only_their_own_newsletter(self):
        token1 = self.get_token("journalist")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token1}")

        create_response = self.client.post("/api/newsletters/create/", {
            "title": "J1 Newsletter",
            "description": "Owned by J1"
        })

        newsletter_id = create_response.data["id"]

        token2 = self.get_token("journalist2")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token2}")

        delete_response = self.client.delete(f"/api/newsletters/{newsletter_id}/delete/")
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_journalist_can_add_article_to_newsletter(self):
        token_j = self.get_token("journalist")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_j}")

        article_response = self.client.post("/api/articles/create/", {
            "title": "Article 1",
            "content": "Content",
            "publisher": self.publisher.id
        })

        article_id = article_response.data["id"]

        newsletter_response = self.client.post("/api/newsletters/create/", {
            "title": "Weekly",
            "description": "Desc"
        })

        newsletter_id = newsletter_response.data["id"]

        add_response = self.client.post(f"/api/newsletters/{newsletter_id}/add-article/", {
            "article_id": article_id
        })

        self.assertEqual(add_response.status_code, status.HTTP_200_OK)


# =========================================================
# SUBSCRIPTION TESTS
# =========================================================

class SubscriptionAPITest(BaseAPITest):

    def test_reader_can_subscribe_to_publisher(self):
        token = self.get_token("reader")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(f"/api/publishers/{self.publisher.id}/subscribe/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.publisher, self.reader.subscriptions_publishers.all())

    def test_reader_can_unsubscribe_from_publisher(self):
        self.reader.subscriptions_publishers.add(self.publisher)

        token = self.get_token("reader")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(f"/api/publishers/{self.publisher.id}/unsubscribe/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.publisher, self.reader.subscriptions_publishers.all())

    def test_reader_can_subscribe_to_journalist(self):
        token = self.get_token("reader")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(f"/api/journalists/{self.journalist.id}/subscribe/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.journalist, self.reader.subscriptions_journalists.all())

    def test_reader_can_unsubscribe_from_journalist(self):
        self.reader.subscriptions_journalists.add(self.journalist)

        token = self.get_token("reader")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(f"/api/journalists/{self.journalist.id}/unsubscribe/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.journalist, self.reader.subscriptions_journalists.all())

    def test_subscribed_articles_feed_returns_correct_articles(self):
        # Journalist 1 creates article for publisher 1
        token_j1 = self.get_token("journalist")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_j1}")

        article1 = self.client.post("/api/articles/create/", {
            "title": "Tech News",
            "content": "Tech content",
            "publisher": self.publisher.id
        }).data

        # Journalist 2 creates article for publisher 2
        token_j2 = self.get_token("journalist2")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_j2}")

        article2 = self.client.post("/api/articles/create/", {
            "title": "Sports News",
            "content": "Sports content",
            "publisher": self.publisher2.id
        }).data

        # Reader subscribes to publisher 1 only
        token_r = self.get_token("reader")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_r}")

        self.client.post(f"/api/publishers/{self.publisher.id}/subscribe/")

        # Fetch subscribed articles
        response = self.client.get("/api/articles/subscribed/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should contain only article1
        returned_titles = [a["title"] for a in response.data]
        self.assertIn("Tech News", returned_titles)
        self.assertNotIn("Sports News", returned_titles)


# =========================================================
# APPROVED SIGNAL ENDPOINT TEST
# =========================================================

class ApprovedSignalAPITest(BaseAPITest):

    def test_approved_signal_endpoint_accepts_post(self):
        token = self.get_token("editor")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post("/api/approved/", {
            "article_id": 1,
            "status": "approved"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Signal received")
