from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField 
#from django.db.models.signals import post_save
#from django.dispatch import receiver
#import json
#from django_celery_beat.models import PeriodicTask, CrontabSchedule


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20, default="", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='category')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reg_user')
    title = models.CharField(max_length=100, default="", null=True, blank=True)
    description = RichTextUploadingField(default="", blank=True, null=True)
    file_upload = models.FileField(default=None, upload_to=f'{category}/', blank=True, null=True)
    photo = models.ImageField(upload_to=f'media/blog/{category.name}/', default="")
    is_posted = models.BooleanField(default=True, null=True, blank=True)
    user_like_post = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_like')
    date_publish = models.DateTimeField(blank = True, null = True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='post')
    #user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(default="", null=True, blank=True)
    comment = models.TextField(default="", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post.title

class PostViews(models.Model):
    postview = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='postview')
    views_count = models.IntegerField(default=0)

class Newletter(models.Model):
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.email

