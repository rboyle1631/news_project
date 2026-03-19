News Project — Django REST API
A Django-based news management API featuring role-based access, JWT authentication, Sphinx documentation, and Dockerized deployment.
This project was built as part of the HyperionDev Software Engineering Bootcamp (Capstone).

Features
Django REST Framework API

JWT Authentication (login, register)

Role-based permissions (Admin, Editor, Reader)

CRUD operations for news articles

MariaDB database support

Dockerized backend

Full Sphinx documentation included in the repo

Automated management command for role setup

Project Structure
Code
news_project/
    newsapp/
    docs/
        _build/html/   ← Generated Sphinx documentation
    Dockerfile
    requirements.txt
    manage.py
Installation (Local)
1. Clone the repository
Code
git clone <your-repo-url>
cd news_project
2. Create and activate a virtual environment
Code
python -m venv venv
venv\Scripts\activate
3. Install dependencies
Code
pip install -r requirements.txt
4. Create your .env file
Copy the example:

Code
cp .env.example .env
Update values as needed.
Fallback values are included to prevent crashes if variables are missing.

5. Run migrations
Code
python manage.py migrate
6. Create a superuser
Code
python manage.py createsuperuser
7. Start the server
Code
python manage.py runserver
Running with Docker
1. Build the image
Code
docker build -t news_project .
2. Run the container
Code
docker run -p 8000:8000 news_project
3. Access the API
Code
http://localhost:8000/api/
Running Tests
Code
python manage.py test
Documentation
Full Sphinx documentation is included in the repository:

Code
docs/_build/html/index.html
Open it in your browser to view:

Code
file:///path/to/repo/docs/_build/html/index.html
Authentication
This project uses JWT authentication.

Obtain Token
Code
POST /api/token/
Refresh Token
Code
POST /api/token/refresh/
Include the token in all authenticated requests:

Code
Authorization: Bearer <your-token>
📡 API Endpoints (Plain Text for Submission)
Authentication
Code
POST /api/token/
POST /api/token/refresh/
Articles
Code
GET    /api/articles/
POST   /api/articles/
GET    /api/articles/<id>/
PUT    /api/articles/<id>/
DELETE /api/articles/<id>/
Users / Roles
Code
POST /api/register/
GET  /api/users/
Management Commands
Setup default roles
Code
python manage.py setup_roles
Creates:

Admin

Editor

Reader

Environment Variables
Your .env file should include:

Code
SECRET_KEY=
DEBUG=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=
Fallback values are used if missing.

MariaDB Configuration
If using MariaDB:

Code
ENGINE=django.db.backends.mysql
NAME=newsdb
USER=root
PASSWORD=yourpassword
HOST=localhost
PORT=3306
Author
Russell Boyle  
