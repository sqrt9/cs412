# Models.py
# Theodore Harlan
# hpt@bu.edu
# Created Feb. 12
# Modified Feb. 20

from django.db import models
from django.utils import timezone
import json

# Create your models here.

class Profile(models.Model):
    """
    Model for user profile in mini insta app
    containing minimal info about a user
    """
    
    username     = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=150)
    icon         = models.URLField(blank=True)
    bio          = models.TextField(blank=True)
    joined       = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """
        Build a string representation of a user.
        """
        
        return json.dumps(
            {
                "username"    : self.username,
                "display_name": self.display_name,
                "icon"        : self.icon,
                "bio"         : self.bio,
                "joined"      : self.joined.isoformat()
            }
        )
        

class Post(models.Model):
    """
    Model for the post relation.
            * timestamp        - date of upload
            * caption          - user provided photo title
            * profile          - post author
    """
    
    timestamp = models.DateField(default=timezone.now)
    caption   = models.CharField(max_length=20)
    profile   = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    def __str__(self):
        """
        Build a string representation of a post.
        """
        
        return json.dumps(
            {
                "timestamp": self.timestamp.isoformat(),
                "caption"  : self.caption,
                "profile"  : self.profile.display_name
            }
        )

class Photo(models.Model):
    """
    Model for photo objects
        Fields:
            * loc              - location of image
            * desc             - user provided photo desciption
            * username         - username of author

    """
    
    loc       = models.URLField()
    post      = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateField(default=timezone.now)
    
    def __str__(self):
        """
        Build a string representation of the photo object.
        """
        
        return json.dumps(
            {
                "loc"     : self.loc,
                "desc"    : self.timestamp.isoformat(),
                "username": self.post.profile.username
            }
        )
