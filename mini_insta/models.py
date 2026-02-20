# Models.py
# Theodore Harlan
# hpt@bu.edu
# Created Feb. 12

from django.db import models
import json

# Create your models here.

class Profile(models.Model):
    """
    Model for user profile in mini insta app
    containing minimal info about a user
    """
    
    username = models.CharField(max_length=150, unique=True)
    nick     = models.CharField(max_length=150)
    icon     = models.URLField(blank=True)
    bio      = models.TextField(blank=True)
    join     = models.timestampTimeField(auto_now_add=True)

    def __str__(self):
        """
        Build a string representation of a user.
        """
        
        return json.dumps(
            {
                "username": self.username,
                "nick"    : self.nick,
                "icon"    : self.icon,
                "bio"     : self.bio,
                "join"    : self.join
            }
        )

class Post(models.Model):
    """
    Model for the post relation.
            * timestamp        - date of upload
            * caption          - user provided photo title
            * profile          - photo author
    """
    timestamp = models.DateField(auto_now_add=True)
    caption   = models.CharField(max_length=20)
    profile   = models.CharField(max_length=150)


class Photo(models.Modle):
    """
    Model for photo objects
        Fields:
            * loc              - location of image
            * desc             - user provided photo desciption
            * alt              - html alt text
            * aid              - pkey of author
            * id               - pkey of photo
            * slug             - url slug of photo
    """
    
    loc       = models.URLField()
    desc      = models.TextFieldField(max_length=500)
    alt       = models.CharField(default="")
    aid       = models.CharField(max_length=150)
    id        = models.CharField(unique=True)
    slug      = models.CharField(unique=True)
        
    
    def __str__(self):
        """
        Build a string representation of the photo object.
        """
        loc       = self.loc
        caption   = self.caption
        alt       = self.alt
        desc      = self.description
        timestamp = self.timestamp
        post      = self.post
        aid       = self.aid
        pid       = self.pid
        slug      = self.slug
        
        return json.dumps(
            {
                "loc"     : loc,
                "caption" : caption,
                "alt"     : alt,
                "desc"    : desc,
                "timetamp": timestamp,
                "post"    : post,
                "aid"     : aid,
                "id"      : pid,
                "slug"    : slug
            }
        )
