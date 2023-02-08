from django.db import models

# Create your models here.

class ContactData(models.Model):
    name = models.CharField(default="", blank=True, null=True, max_length=50)
    email = models.EmailField(null=True, blank=True)
    phone_no = models.IntegerField(null=True, blank=True)
    text = models.TextField(default="", null=True, blank=True)

    def __str__(self):
        return self.name