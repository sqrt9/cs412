from rest_framework import serializers
from .models import Profile, Post, Photo, Follow, Like
 
 
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Photo
        fields = ["id", "media"]
 
 
class ProfileSerializer(serializers.ModelSerializer):
    """Lightweight profile — used when embedded inside other objects."""
    class Meta:
        model  = Profile
        fields = ["id", "username","display_name", "bio", "icon"]
 
 
class PostSerializer(serializers.ModelSerializer):
    photos  = PhotoSerializer(many=True, read_only=True, source="photo_set")
    profile = ProfileSerializer(read_only=True)
    likes   = serializers.SerializerMethodField()
 
    class Meta:
        model  = Post
        fields = ["id", "profile", "caption", "timestamp", "photos", "likes"]
 
    def get_likes(self, obj):
        return obj.like_set.count()
 
 
class PostCreateSerializer(serializers.ModelSerializer):
    """Write-only serializer used when creating a new post via the API."""
    class Meta:
        model  = Post
        fields = ["caption"]