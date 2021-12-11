from django.db import models
from django.contrib.auth.models import User

# Create your models here.
"""
A profile model for each user that is logged into the app
"""
class Profile(models.Model):
    username = models.CharField(max_length=100, blank=True)
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    pfp = models.ImageField(upload_to='images/', blank=True)
    bio = models.TextField(blank=True)
    friends = models.ManyToManyField(User, related_name="friends")

    def __str__(self):
        return f'{self.user.username}'
