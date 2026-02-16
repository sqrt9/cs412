# Models.py
# Theodore Harlan
# hpt@bu.edu
# Created Feb. 12

from django.db import models

# Create your models here.
class Profile(models.Model):
    username = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=150)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name or self.username