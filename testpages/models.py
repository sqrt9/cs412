from django.db import models

# Create your models here.

# Basic testing models

class TestList(models.Model):
    testListDesc = models.CharField(max_length=50);

class TestModel(models.Model):
    testInt = models.IntegerField();
    testChar = models.CharField(max_length=50);
    testList = models.ForeignKey(TestList, on_delete=models.CASCADE)

# Data Models

class CollectionArtist(models.Model):
    collectionArtistName        = models.CharField(max_length=128);
    collectionArtistLocation    = models.CharField(max_length=128);
    collectionArtistDescription = models.CharField(max_length=128);

class CollectionTrack(models.Model):
    trackFile = models.FileField()

class Collection(models.Model):
    collectionTitle       = models.CharField(max_length=128)
    collectionDescription = models.CharField(max_length=500)
    collectionMediaType   = models.CharField(max_length=128)
    collectionArtist      = models.ManyToManyField(CollectionArtist)
    collectionTracks      = models.ManyToManyField(CollectionTrack)
    collectionYear        = models.IntegerField()
    collectionTracks      = models.IntegerField()
    collectionDisks       = models.IntegerField()
    collectionFiles       = models.FileField();
    collectionCover       = models.ImageField();

class CollectionGenreDescriptor(models.Model): 
    collections = models.ForeignKey(Collection, on_delete=models.CASCADE)
    artists     = models.ForeignKey(CollectionArtist, on_delete=models.CASCADE)
    descriptor  = models.CharField(max_length=128)
