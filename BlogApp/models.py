from django.db import models
# from django.contrib.auth.models import AbstractUser 
from django.contrib.auth.models import AbstractUser 
from django.conf import settings

class CustomUser (AbstractUser):
    email_token = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class BlogModel(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()
    image=models.ImageField(upload_to='Blog_media/')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
