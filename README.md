# 📰 News Project API

A Django REST Framework application for publishing articles, managing newsletters, subscribing to publishers or journalists, and receiving curated content.  
Includes JWT authentication, role‑based access, Docker support, and full Sphinx documentation.

---

## 📑 Table of Contents
- [Features](#-features)
- [Installation](#️-installation)
- [Docker Setup](#-docker-setup)
- [Documentation](#-documentation)
- [Authentication](#-authentication)
- [API Endpoints](#-api-endpoints)
- [Management Commands](#-management-commands)
- [Author](#-author)

---

## ✨ Features
- Create, update, and delete news articles  
- Manage newsletters and attach articles  
- Subscribe/unsubscribe to publishers and journalists  
- Personalized feed of subscribed content  
- JWT authentication for secure access  
- Automated role setup via management command  
- Sphinx-generated documentation included  

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/rboyle1631/news_project
cd news_project
```

### 2. Create virtual environment
```bash
py -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
py manage.py migrate
```

### 5. Start the development server
```bash
py manage.py runserver
```

## 🐳 Docker Setup

### Build the Docker image
```bash
docker build -t news_project .
```
### Run the container

```bash
docker run -p 8000:8000 news_project
```

## 📚 Documentation

### Open Sphinx HTML docs
```bash
docs/_build/html/index.html
```

## 🔐 Authentication

### Obtain JWT token
POST /api/token/

### Refresh token
POST /api/token/refresh/

### Authorization header format
Authorization: Bearer <your_token>

## 🛠 API Endpoints

### Article endpoints
POST /api/articles/create/  
PUT /api/articles/<id>/update/  
DELETE /api/articles/<id>/delete/

### Newsletter endpoints
POST /api/newsletters/create/  
PUT /api/newsletters/<id>/update/  
DELETE /api/newsletters/<id>/delete/  
POST /api/newsletters/<id>/add-article/

### Subscription endpoints
POST /api/publishers/<id>/subscribe/  
POST /api/publishers/<id>/unsubscribe/  
POST /api/journalists/<id>/subscribe/  
POST /api/journalists/<id>/unsubscribe/

### Reader feed
GET /api/articles/subscribed/

### Signals
POST /api/approved/

## 🧰 Management Commands

### Setup default roles
```bash
python manage.py setup_roles
```

## 👤 Author

Russell Boyle
