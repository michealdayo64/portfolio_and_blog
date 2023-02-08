from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField 
from django.conf import settings

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=20, default="", null=True, blank=True)
    description = RichTextUploadingField(default="", blank=True, null=True)
    github_link = models.URLField(default="", null=True, blank=True)
    img = models.ImageField(default="", upload_to="portfolio/")
    user_like_proj = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_like_proj')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ProjectComment(models.Model):
    post = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='project')
    #user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(default="", null=True, blank=True)
    comment = models.TextField(default="", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class ProjectViews(models.Model):
    postview = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='projectview')
    views_count = models.IntegerField(default=0)