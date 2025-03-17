from django.contrib import admin
from .models import User, Category, BlogPost, Like, Review

admin.site.register(User)
admin.site.register(Category)
admin.site.register(BlogPost)
admin.site.register(Like)
admin.site.register(Review)