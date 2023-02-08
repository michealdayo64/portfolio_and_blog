from django.contrib import admin
from .models import Category, Post, PostComment, PostViews, Newletter

# Register your models here.
admin.site.register([Category, Post, PostComment, PostViews, Newletter])
