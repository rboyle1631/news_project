News Platform API
A role‑based news publishing API built with Django and Django REST Framework. The system supports article publishing, newsletter management, and reader subscription features, with strict permission rules enforced through automated tests.

Features
Articles
Journalists can create, update, and delete their own articles.

Editors can update and delete any article.

Readers cannot create or modify articles.

Articles may optionally belong to a publisher.

Newsletters
Journalists can create newsletters and manage their own newsletters.

Editors can update and delete any newsletter.

Readers cannot create newsletters.

Journalists can add articles to their own newsletters.

Subscriptions
Readers can subscribe/unsubscribe to:

Publishers

Journalists

Subscribed readers receive a combined feed of:

Articles from subscribed publishers

Articles from subscribed journalists

Signals
An endpoint exists to receive “approved” article signals.

This project uses a dry‑run mode (no external API calls).

API Endpoints (Plain Text Version)
Articles
POST /api/articles/create/ — Create an article (Journalist)

PUT /api/articles/<id>/update/ — Update an article (Journalist: own, Editor: any)

DELETE /api/articles/<id>/delete/ — Delete an article (Journalist: own, Editor: any)

Newsletters
POST /api/newsletters/create/ — Create a newsletter (Journalist)

PUT /api/newsletters/<id>/update/ — Update a newsletter (Journalist: own, Editor: any)

DELETE /api/newsletters/<id>/delete/ — Delete a newsletter (Journalist: own, Editor: any)

POST /api/newsletters/<id>/add-article/ — Add article to newsletter (Journalist: own)

Publisher Subscriptions
POST /api/publishers/<id>/subscribe/ — Subscribe to publisher (Reader)

POST /api/publishers/<id>/unsubscribe/ — Unsubscribe from publisher (Reader)

Journalist Subscriptions
POST /api/journalists/<id>/subscribe/ — Subscribe to journalist (Reader)

POST /api/journalists/<id>/unsubscribe/ — Unsubscribe from journalist (Reader)

Reader Feed
GET /api/articles/subscribed/ — Get articles from subscriptions (Reader)

Signals
POST /api/approved/ — Receive approved‑article signal