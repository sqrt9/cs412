# Models.py
# Theodore Harlan
# hpt@bu.edu
# Created Feb. 12
# Modified Feb. 20
# Description:
# ---
# Models representing the relations and database objects
# for the mini_insta app.
# ---

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
    
    def get_absolute_url(self):
        """
        Return the URL of the profile (used by UpdateProfileView)
        on successful form submissions on Profile models.
        """
        return "/mini_insta/profile/" + str(self.id)
    
    @property
    def get_followers(self):
        """
        Get the list of followers for this Profile
        """
        return [f.followee for f in self.followers.all()]

    @property
    def get_num_followers(self):
        """
        Get the number of followers for this Profile
        """
        return self.followers.count()

    @property
    def get_following(self):
        """
        Get the followers of this Profile
        """
        return [f.follower for f in self.followees.all()]

    @property
    def get_num_following(self):
        """
        Get the number of people following this Profile
        """
        return self.followees.count()
    
    @property
    def get_feed_posts(self):
        """
        Return posts by Profiles this Profile is following
        """
        from .models import Post
        return Post.objects.filter(profile__followers__followee=self)

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
    
    @property
    def get_likes(self):
        """
        Return a list of profile names that like this post
        """
        return [like for like in self.like_set.all()]

    @property
    def get_like_count(self):
        """
        Return a number of likes on this post
        """
        return self.like_set.count()
    
    @property
    def get_comments(self):
        """
        Return all comment models associated with this post
        """
        return self.comment_set.all()
    
    @property
    def get_num_comments(self):
        """
        Return number of comments on this post
        """
        return self.comment_set.count()
        

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
    
    loc       = models.URLField(blank=True)
    media     = models.ImageField(default="")
    post      = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateField(default=timezone.now)
    
    def __str__(self):
        """
        Build a string representation of the photo object.
        """
        
        return json.dumps(
            {
                "media"   : self.get_image_url,
                "desc"    : self.timestamp.isoformat(),
                "username": self.post.profile.username
            }
        )
    
    @property
    def get_image_url(self):
        """
        Retrieve local media or from URL associated with a photo.
        """
        if self.loc:
            return self.loc
        elif self.media:
            return self.media.url
        else:
            return ""
    
    
    
class Follow(models.Model):
    """
    Model for following relationship.
    Fields:
        * Follower         - Profile that began the relation
        * Followee         - Profile being followed
        * Timestamp        - Time the relation began
    """
    follower  = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="followers")
    followee  = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="followees")
    timestamp = models.DateTimeField()
    
    def __str__(self):
        """
        Return a string representation of a following relationship.
        """
        return json.dumps(
            {
                "follower" : self.follower.username,
                "followee" : self.followee.username,
                "timestamp": self.timestamp.isoformat()
            }
        )

class Comment(models.Model):
    """
    Model for post comments.
    Fields:
        * Profile           - User who posted the comment
        * Post              - Post the comment's on
        * Timestamp         - Time of comment
        * Text              - Text of the comment
    """
    
    profile   = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post      = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    text      = models.TextField()
    
    def __str__(self):
        """
        Return a string representation of the comment.
        """
        return json.dumps(
            {
                "profile"  : self.profile.username,
                "post"     : self.post.caption,
                "timestamp": self.timestamp.isoformat(),
                "text"     : self.text 
            }
        )
        
class Like(models.Model):
    """
    Model for post likes.
    """
    
    post      = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile   = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    
    def __str__(self):
        """
        Return a string representation of a like.
        """
        return json.dumps(
            {
                "profile"  : self.profile.username,
                "post"     : self.post.caption,
                "timestamp": self.timestamp.isoformat()
            }
        )
