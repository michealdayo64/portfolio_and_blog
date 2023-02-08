from django.contrib import admin
from .models import Project, ProjectComment

# Register your models here.
admin.site.register([Project, ProjectComment])
