from django.db import models
from django.utils import timezone
from profiles.models import Profile
from django.contrib.auth.models import User

# Create your models here.
"""
A place model for each building on Grounds
"""
class Place(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True)
    address = models.CharField(max_length=100, default="")
    description = models.TextField(blank=True)
    num_likes = models.IntegerField(default=0)
    likes = models.ManyToManyField(Profile, related_name="likes")

    def __str__(self):
        return f'{self.name}'
"""
Review model that users make under each Place
# """
class Review(models.Model):
    author = models.ForeignKey(Profile, related_name="reviews", on_delete=models.CASCADE, default=1)
    place = models.ForeignKey(Place,related_name="reviews", on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(default = timezone.now)

    #needed for most recent views
    class Meta:
        ordering = ['created_on']
    
    def __str__(self):
        return f'Review {self.content} Review {self.author}'

# """
# Ratings model that will hold each user's rating for a place
# """ 
# class Rating(models.Model):
#     place = models.ForeignKey(Place, related_name="ratings", on_delete=models.CASCADE)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     number = models.IntegerField(default=5)