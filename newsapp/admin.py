from django.contrib import admin
from .models import User, Publisher, Article, Newsletter

admin.site.register(User)
admin.site.register(Publisher)
admin.site.register(Article)
admin.site.register(Newsletter)
