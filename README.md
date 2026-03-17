News Platform API
A role‑based news publishing API built with Django and Django REST Framework.
The system supports article publishing, newsletter management, reader subscriptions, and an external “approved article” signal endpoint — all enforced through strict permission rules and automated tests.

Features
Articles
Journalists can create, update, and delete their own articles.

Editors can update and delete any article.

Readers cannot create or modify articles.

Articles may optionally belong to a Publisher.

Newsletters
Journalists can create and manage their own newsletters.

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
An endpoint exists to receive “approved article” signals from external systems.

This project uses a dry‑run mode (no external API calls).

API Endpoints
Articles
Method	Endpoint	Description	Roles
POST	/api/articles/create/	Create an article	Journalist
PUT	/api/articles//update/	Update an article	Journalist (own), Editor (any)
DELETE	/api/articles//delete/	Delete an article	Journalist (own), Editor (any)
Newsletters
Method	Endpoint	Description	Roles
POST	/api/newsletters/create/	Create a newsletter	Journalist
PUT	/api/newsletters//update/	Update a newsletter	Journalist (own), Editor (any)
DELETE	/api/newsletters//delete/	Delete a newsletter	Journalist (own), Editor (any)
POST	/api/newsletters//add-article/	Add article to newsletter	Journalist (own)
Publisher Subscriptions
Method	Endpoint	Description	Roles
POST	/api/publishers//subscribe/	Subscribe to publisher	Reader
POST	/api/publishers//unsubscribe/	Unsubscribe from publisher	Reader
Journalist Subscriptions
Method	Endpoint	Description	Roles
POST	/api/journalists//subscribe/	Subscribe to journalist	Reader
POST	/api/journalists//unsubscribe/	Unsubscribe from journalist	Reader
Reader Feed
Method	Endpoint	Description	Roles
GET	/api/articles/subscribed/	Get articles from subscriptions	Reader
Signals
Method	Endpoint	Description
POST	/api/approved/	Receive approved‑article signal
Docker Support
This project includes a full Docker setup.

Pull the image
Code
docker pull rboyle1631/news_project:latest
Run the container
Code
docker run -p 8000:8000 rboyle1631/news_project:latest
API will be available at:

Code
http://localhost:8000
Project Structure
Code
news_project/
newsapp/
docs/
Dockerfile
requirements.txt
manage.py
Documentation
Sphinx documentation is included in the docs/ directory.

Build docs:

Code
cd docs
make html
