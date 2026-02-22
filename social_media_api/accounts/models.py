from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class useraccounts(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    followers = models.ManyToManyField('self', blank=True, related_name='following', symmetrical=False)

    def __str__(self):
        return self.username

    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.url
        return None