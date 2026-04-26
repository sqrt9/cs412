from django.db import models
from django.contrib.auth.models import User
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from django.core.files.base import ContentFile

# Create your models here.
# Basic testing models
# Data Models

class Profile(models.Model):
    """Site user model. Accompanied with a django user"""
    user = models.OneToOneField(
                                User,
                                on_delete    = models.CASCADE,
                                related_name = "django_user"
                                )
        # contains other info too, such as
        #       join_date
        #       username
        #       first_name
        #       last_name
        # which is not needed here

    display_name        = models.CharField(max_length=32, default="")
    profile_icon        = models.ImageField()
    profile_description = models.TextField(max_length=1000)
    
    #some passthrough methods to access django user info on a profile
    @property
    def join_date(self):
        return self.user.join_date
    @property
    def username(self):
        return self.user.username
    @property
    def name(self):
        return self.user.first_name + " " + self.user.last_name

class Artist(models.Model):
    """Musical artist model"""
    name        = models.CharField(max_length=128)
    description = models.TextField(max_length=1000, blank=True)


class Album(models.Model):
    """
    Model for a singular music album. Metadata comes from tracks.
    User uploaded albums are associated with a profile. 
    Let the uploader be null for music uploaded by the site admins
    """
    name     = models.CharField(max_length=256)
    uploader = models.ForeignKey(
                                Profile,
                                on_delete = models.CASCADE,
                                null      = True,
                                blank     = True
                                )
    artist      = models.ForeignKey(Artist, on_delete=models.CASCADE)
    is_official = models.BooleanField(default=False)
    is_private  = models.BooleanField(default=True)
    
    @property
    def cover(self):
        first = self.tracks.order_by('disc_number', 'track_number').first()
        if first and first.track_cover:
            return first.track_cover.url
        return None


class Track(models.Model):
    """
    Model for a single track
    Only relations and media file fields are here.
    Track info and everything else is stored in-file.
    'populate' method sets up the relation because the
    artists are not guaranteed to exist yet if this is a
    new file. So we allow them to be null/blank and
    call 'get_or_create' when populating
    """
    
    album = models.ForeignKey(
        Album,
        on_delete    = models.CASCADE,
        related_name = "tracks",
        blank        = True,
        null         = True
        )
    artist = models.ForeignKey(
        Artist,
        on_delete    = models.CASCADE,
        related_name = "artist_tracks",
        blank        = True,
        null         = True
        )
    features = models.ManyToManyField(
        Artist,
        related_name = "features",
        blank        = True
        )

    track_number = models.PositiveIntegerField(null=True, blank=True)
    disc_number  = models.PositiveIntegerField(null=True, blank=True)
    track_file  = models.FileField()
    track_cover = models.ImageField(upload_to="covers/",
                                    null=True,
                                    blank=True)
    
    def populate(self, user=None, private=True):
        """
        When entering a new track, assume the following:
            - This track has one primary artist             (id3_albumartist)
            - This track belongs on one album               (id3_album)
            - This track may have multiple featured artists (id3_artists)
        Then,
            - Set up the "features" M2M, "artist" and "album" M2O,
              create these models if they dont exist yet
        """
        tags            = dict(EasyID3(self.track_file.path).items())
        id3_album       = tags.get("album", "Unknown Album")[0]
        id3_albumartist = tags.get("albumartist", "Unknown Artist")[0]
        id3_artists     = tags.get("artist", [])
        id3_cover       = ID3(self.track_file.path).get('APIC:')
                                # APIC - Attached PICture

        if id3_cover:           # written as image/jpeg, image/png, etc.
            id3_cover_extension = id3_cover.mime.split('/')[-1]
            self.track_cover    = ContentFile(
                                    id3_cover.data,
                                    name=f'{self.pk}_cover.{id3_cover_extension}')
        
        id3_track  = tags.get("tracknumber", ["0"])[0].split('/')[0]
        id3_disc   = tags.get("discnumber",  ["1"])[0].split('/')[0]
        self.track_number = int(id3_track) if id3_track.isdigit() else None
        self.disc_number  = int(id3_disc)  if id3_disc.isdigit()  else None
        
        for f in id3_artists:
            # don't mark a feature if they're already the primary artist
            if f != id3_albumartist: 
                feature, _  = Artist.objects.get_or_create(name=f)
                self.features.add(feature)
        
        artist, _ = Artist.objects.get_or_create(name=id3_albumartist)
        album, _ = Album.objects.get_or_create(
            name       = id3_album,
            artist     = artist,
            uploader   = user,
            is_private = private,
            defaults   = { # used on creating
                'is_official': False if user else True
            }
        )
        self.album = album
        self.artist = artist
        self.save()

    @property
    def url(self):
        """Online url serving this file"""
        return self.track_file.url
    
    @property
    def tags(self):
        """Return ID3 tags dictionary"""
        return dict(EasyID3(self.track_file.path).items())
    