from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


'''class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user'''
    

def get_profile_image_path(self):
    return f'profile_image/{self.username}/'

def get_default_profile_image():
    return f'mikkytechie/avatar.jpeg'

class Account(AbstractUser):
    #email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    #username = models.CharField(max_length=30, unique=True)
    photo = models.ImageField(upload_to=get_profile_image_path, default=get_default_profile_image, null=True, blank=True)
    #is_admin = models.BooleanField(default=False)
    #is_superuser = models.BooleanField(default=True)
    #is_active = models.BooleanField(default=False)
    #date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date join')
    #last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    
    '''USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = MyAccountManager()'''
    

