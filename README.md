News Platform API
A role‑based news publishing API built with Django and Django REST Framework.
The platform supports article publishing, newsletter management, reader subscriptions, and an external “approved article” signal endpoint.
Strict permission rules are enforced through automated tests.

Project Overview
This API provides:

Role‑based access control (Reader, Journalist, Editor)

Article creation and editorial workflow

Newsletter creation and article assignment

Reader subscription system (publishers + journalists)

Combined subscription feed

Dry‑run signal endpoint for external integrations

Full Sphinx documentation

Docker support

Separate Git branches for documentation and containerization

Getting Started
Clone the Repository
Code
git clone https://github.com/rboyle1631/news_project.git
cd news_project
Create & Activate a Virtual Environment
Code
python -m venv venv
.\venv\Scripts\activate
Install Dependencies
Code
pip install -r requirements.txt
Environment Variables
Create a .env file in the project root:

Code
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_NAME=newsdb
DATABASE_USER=root
DATABASE_PASSWORD=yourpassword
DATABASE_HOST=localhost
DATABASE_PORT=3306
(Adjust as needed for your MariaDB setup.)

Run Migrations
Code
python manage.py migrate
Start the Development Server
Code
python manage.py runserver
API will be available at:

Code
http://localhost:8000
Running with Docker
Pull the image
Code
docker pull rboyle1631/news_project:latest
Run the container
Code
docker run -p 8000:8000 rboyle1631/news_project:latest
📚 Documentation (Sphinx)
Documentation source files are located in:

Code
docs/
To build the docs locally:

Code
cd docs
.\make.bat html
Generated HTML will appear in:

Code
docs/_build/html/
This folder is included in the repository for assessor review.

Git Branch Structure
Branch	Purpose
master	Main development branch
docs	Sphinx documentation setup + generated HTML
container	Dockerfile and containerization work

All required branches are pushed to GitHub as per task instructions.

Roles & Permissions
Reader
Subscribe/unsubscribe to publishers

Subscribe/unsubscribe to journalists

View combined subscription feed

Cannot create or modify content

Journalist
Create/update/delete own articles

Create/update/delete own newsletters

Add articles to own newsletters

Editor
Update/delete any article

Update/delete any newsletter

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
POST	/api/approved/	Receive approved‑article signal (dry‑run mode)

Signals
Method	Endpoint	Description
POST	/api/approved/	Receive approved‑article signal (dry‑run mode)
