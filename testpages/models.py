from django.db import models
from django.contrib.auth.models import User
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from django.core.files.base import ContentFile
import musicbrainzngs
import requests
from rapidfuzz import fuzz
from time import sleep
from pathlib import Path

# Create your models here.

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
    profile_icon        = models.ImageField(blank=True)
    profile_description = models.TextField(max_length=1000, blank=True)
    
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
    
    def populate(self):
        pass


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
    mbid        = models.CharField(blank=True)
    
    def populate(self):
        pass
    
    @property
    def cover(self):
        first = self.tracks.order_by('disk_number', 'track_number').first()
        if first and first.track_cover:
            return first.track_cover.url
        return None
    
    @classmethod
    def match(cls, album_name=None, artist_name=None, mbid=None):
        """
        Find an Album by mbid if provided, otherwise by album and artist name.
        Returns the Album instance or None.
        """
        if mbid:
            return cls.objects.filter(mbid=mbid).first()
        
        if album_name and artist_name:
            return cls.objects.filter(
                name__iexact=album_name,
                artist__name__iexact=artist_name
            ).first()
        
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
    
    track_title = models.CharField()
    track_number = models.PositiveIntegerField(null=True, blank=True)
    track_length = models.PositiveIntegerField(null=True, blank=True)
    disk_number  = models.PositiveIntegerField(null=True, blank=True)
    track_file  = models.FileField()
    track_cover = models.ImageField(upload_to="covers/",
                                    null=True,
                                    blank=True
                                    )
    
    
    def populate(self,
                 user    = None,
                 private = False,
                 search  = False,   # let users decide if the album info they
                                    # provided should be used to search the internet
                 from_file = False):
        """
        When entering a new track, assume the following:
            - This track has one primary artist             (id3_albumartist)
            - This track belongs on one album               (id3_album)
            - This track may have multiple featured artists (id3_artists)
        Then,
            - Set up the "features" M2M, "artist" and "album" M2O,
              create these models if they dont exist yet
        """
        
        update_album = None
            # populate returns a set of pks to albums that were updated.
            # if using the search function, then requests should be made
            # for each one of these albums after the return
        
        self.track_length = int(MP3(self.track_file.path).info.length * 1000)
        
        if from_file:
            tags            = dict(EasyID3(self.track_file.path).items())
            id3_album       = tags.get("album", ["My Songs"])[0]
            id3_albumartist = tags.get("albumartist", ["Various Artists"])[0]
            id3_title       = tags.get("title", ["Untitled"])[0]
            id3_artists     = tags.get("artist", [])
            id3_cover       = ID3(self.track_file.path).get('APIC:')
                                    # APIC - Attached PICture
                                    # written as image/jpeg, image/png, etc.
            if id3_cover:
                id3_cover_extension = id3_cover.mime.split('/')[-1]
                self.track_cover    = ContentFile(
                                        id3_cover.data,
                                        name=f'{self.pk}_cover.{id3_cover_extension}')
            elif search:
                caa_url = get_caaurl_from_id3(id3_album, id3_albumartist)
                caa_image_url = get_caa_image_url(caa_url)
                sleep(1)
                self.write_caa_image_content(caa_image_url)
                

            id3_track  = tags.get("tracknumber", ["0"])[0].split('/')[0]
            id3_disc   = tags.get("discnumber",  ["1"])[0].split('/')[0]
            self.track_number = int(id3_track) if id3_track.isdigit() else 0
            self.track_title  = str(id3_title)
            self.disk_number  = int(id3_disc)  if id3_disc.isdigit()  else 1
            
        
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
                })
            
            update_album = album
            self.album  = album
            self.artist = artist
            
        elif search:
            self.track_title  = Path(self.track_file.name).stem
            # if going purely on search, length and filename are all
            # that we can use to find this track online. match this later

        self.save()
        return update_album


    def write_caa_image_content(self, caa_cover_link):
        """
        Extract the bytes from a link to a Cover
        Art Archive image, and return them.
        """
        try:
            headers = {"User-Agent": "MyDjangoMusicApp/1.0 ( hpt@bu.edu )"}
            res = requests.get(caa_cover_link, headers=headers)
            print(f"CAA image response: {res.status_code}, content-type: {res.headers.get('Content-Type')}")
            if res.status_code == 200:
                content_type    = res.headers.get('Content-Type', 'image/jpeg')
                extension       = content_type.split('/')[-1].split(';')[0].strip()
                caa_cover_bytes = res.content
                print(f"cover bytes length: {len(caa_cover_bytes)}")
                self.track_cover = ContentFile(
                        caa_cover_bytes,
                        name = f'{self.pk}_cover.{extension}'
                        )
            else:
                print(f"CAA image fetch failed: {res.status_code}")
        except Exception as e:
            print(f"write_caa_image_content error: {e}")
            return None


    @property
    def url(self):
        """Online url serving this file"""
        return self.track_file.url
    

def tag_tracks_from_info(album, artist, track_list, user, private):
    """
    Write to a track model's fields using internet
    search based on user-provided info.
    track_list := [("title", Track) ... ]
    """
    
    mbid = get_mbid_from_string(album, artist)
    by_artist, _ = Artist.objects.get_or_create(name=artist)
    on_album = Album.match(mbid=mbid, album_name=album, artist_name=artist)
    
    if on_album:
        print("tracks on album", on_album.name)
        if mbid and not on_album.mbid:
            on_album.mbid = mbid
            on_album.save()
        
        for title, track in track_list:
            track.album = on_album
            track.artist = by_artist
            track.save()
            
    elif mbid:
        print("not on an album, but we have info about it")
        track_album, _  = Album.objects.get_or_create(
                                                name     = album,
                                                artist   = by_artist,
                                                mbid     = mbid,
                                                defaults = {
                                                        'uploader': user,
                                                        'is_private': private
                                                    })
        sleep(1)
        track_info, mb_title, mb_artist, mb_rg_mbid = get_track_list_from_mbid(mbid)
        if not track_info:
            print("got nothing")
            return

        album_name  = mb_title  or album
        artist_name = mb_artist or artist
        print(f"MB album: {album_name}, MB artist: {artist_name}")

        track_album.name = album_name
        track_album.save()

        by_artist.name = artist_name
        by_artist.save()

        # try the specific release first, fall back to release group
        caa_image_url = get_caa_image_url(f"https://coverartarchive.org/release/{mbid}/")
        if not caa_image_url and mb_rg_mbid:
            print("release has no CAA art, falling back to release group")
            caa_image_url = get_caa_image_url(f"https://coverartarchive.org/release-group/{mb_rg_mbid}/")
        print(f"caa_image_url: {caa_image_url}")
        n=0
        for title, track in track_list:
            n += 1
            matched = False
            for mb_track in track_info:
                # if there's a 66% partial match on the title, and the duration is
                # within 15 seconds, this is likely the same track
                print("trying title ", title)
                print(fuzz.partial_ratio(mb_track, title), "match")
                print("difference", abs((track.track_length - track_info[mb_track][2])))
                if fuzz.partial_ratio(mb_track, title) >= 66 and \
                    abs((track.track_length - track_info[mb_track][2])) <= 15000:
                        
                    track.track_title  = mb_track
                    track.track_number = n
                    track.disk_number  = 0
                    track.artist       = by_artist
                    track.album        = track_album
                    if caa_image_url and not track.track_cover:
                        track.write_caa_image_content(caa_image_url)
                    track.save()
                    print("matched an online track")
                    print(mb_track)
                    print(track.track_number)
                    print(track.disk_number)
                    matched = True
                    break

            if not matched:
                print("doesn't match anything on the given album")
                track.track_number = 0
                track.disk_number = 1
                track.artist = by_artist # FIX: Just use the object we created at the top
                
                track.album, _  = Album.objects.get_or_create(
                    name=album,
                    artist=by_artist,
                    defaults={
                        'uploader': user,
                        'is_private': private
                    }
                )
                track.save()
                    
    else:
        print("found nothing about this song")
        various_artists, _ = Artist.objects.get_or_create(name="Various Artists")
        my_songs_album, _ = Album.objects.get_or_create(
            name="My Songs",
            artist=various_artists,
            defaults={
                'uploader': user,
                'is_private': private
            }
        )

        for title, track in track_list:
            track.album = my_songs_album
            track.artist = by_artist
            track.save()



#
#
# Helper methods to access APIs
#
#

def get_mbid_from_string(album, artist):
    """
    Get an MBID from an album/artist pair.
    """

    try:
        musicbrainzngs.set_useragent("DjangoMusicApp", "1.0", contact="hpt@bu.edu")
        res = musicbrainzngs.search_releases(
            limit  = 5,
            artistname = artist,
            release = album
            ).get("release-list", [])
        if res:
            official = next((r for r in res if r.get("status") == "Official"), res[0])
            mbid = official["id"]
            return mbid
        return None
    except Exception as e:
        print(e)
        return None

def get_caaurl_from_id3(album, artist):
    """
    Get the link to a cover art archive from the MBID of
    a release. Find find the MBID from tags or user-provided
    info. The musicbrainz release corresponds to a link to CAA. 
    """
    try:
        musicbrainzngs.set_useragent("DjangoMusicApp", "1.0", contact="hpt@bu.edu")
        res = musicbrainzngs.search_releases(
            limit      = 5,
            artistname = artist,
            release    = album
            ).get("release-list", [])
        for release in res:
            if release.get("status") == "Official":
                mbid = release["id"]
                return f"https://coverartarchive.org/release/{mbid}/"
        return None
    except Exception as e:
        print(e)
        return None

def get_caa_image_url(caa_url):
    """
    Get a Cover Art Archive image url from a CAA release link.
    Falls back to the first available image if no 'front' flag exists.
    """
    try:
        headers = {"User-Agent": "MyDjangoMusicApp/1.0 ( hpt@bu.edu )"}
        res = requests.get(caa_url, headers=headers)
        print(f"CAA lookup: {res.status_code} for {caa_url}")
        if res.status_code == 200:
            imgs = res.json().get("images", [])
            if not imgs:
                return None
            for img in imgs:
                if img.get("front"):
                    return img.get("image")
            return imgs[0].get("image")
        return None

    except Exception as e:
        print(f"CAA image error: {e}")
        return None


def get_track_list_from_mbid(mbid):
    try:
        headers = {"User-Agent": "MyDjangoMusicApp/1.0 ( hpt@bu.edu )"}
        res = requests.get(f"https://musicbrainz.org/ws/2/release/{mbid}?inc=recordings&fmt=json", headers=headers)
        mb_tracks  = {}
        mb_title   = None
        mb_artist  = None
        mb_rg_mbid = None
        if res.status_code == 200:
            data       = res.json()
            mb_title   = data.get("title", None)
            mb_artist  = data.get("artist-credit", [{}])[0].get("artist", {}).get("name", None)
            mb_rg_mbid = data.get("release-group", {}).get("id", None)
            media      = data.get("media", [])
            if media:
                for disk in range(len(media)):
                    tracks = media[disk].get("tracks", [])
                    if tracks:
                        for track in tracks:
                            title = track.get("title", None)
                            length = track.get("recording", {}).get("length", None)
                            if title:
                                raw_number   = track.get("number", "0")
                                digits_only  = ''.join(filter(str.isdigit, raw_number))
                                track_number = int(digits_only) if digits_only else 0
                                mb_tracks[title] = (track_number, disk+1, length)
        return mb_tracks, mb_title, mb_artist, mb_rg_mbid
    
    except Exception as e:
        print(e)
        return None, None, None, None