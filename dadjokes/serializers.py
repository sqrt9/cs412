# serializers.py
# Theodore Harlan
# hpt@bu.edu
# Friday April 3rd
# Description: serializers for dadjoke models

from rest_framework import serializers
from .models import Joke, Picture

class JokeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joke
        fields = ['id', 'content', 'contributor', 'timestamp']

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'media', 'timestamp']