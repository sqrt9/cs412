from django.test import TestCase
import requests
import musicbrainzngs
from PIL import Image
from io import BytesIO
from time import sleep
import fuzz

# Create your tests here.


def get_caaurl_from_id3(album, artist):
    """
    Get the link to a cover art archive from the MBID of
    a release. Find find the MBID from tags or user-provided
    info. The musicbrainz release corresponds to a link to CAA. 
    """
    musicbrainzngs.set_useragent("test", "0.000001", contact="hpt@bu.edu")
    try:
        res = musicbrainzngs.search_releases(
            limit  = 5,
            artistname = artist,
            release = album
            ).get("release-list", [])
        for release in res:
            if release.get("status") == "Official":
                mbid = release["id"]
                return f"https://coverartarchive.org/release/{mbid}/" if mbid else None
        return None
    except Exception as e:
        print(e)
        return None

def get_mbid_from_string(album, artist):
    """
    Get an MBID from an album/artist pair.
    """
    musicbrainzngs.set_useragent("test", "0.000001", contact="hpt@bu.edu")
    try:
        res = musicbrainzngs.search_releases(
            limit  = 5,
            artistname = artist,
            release = album
            ).get("release-list", [])
        for release in res:
            if release.get("status") == "Official":
                mbid = release["id"]
                return mbid if mbid else None
        return None
    except Exception as e:
        print(e)
        return None


def get_caa_image_content(caa_cover_link):
    """
    Extract the bytes from a link to a Cover
    Art Archive image, and return them.
    """
    try:
        res = requests.get(caa_cover_link)
        if res.status_code == 200:
            caa_cover_bytes = res.content
            # print(caa_cover_bytes[:20])
            pil_img = Image.open(BytesIO(caa_cover_bytes))
            pil_img.show()
            return None
            # return ContentFile(
            #         caa_cover,
            #         name = f'{self.pk}_cover.jpg'
            #         )
        else:
            return None
    except Exception as e:
        print(e)
        return None

def get_caa_image_url(caa_url):
    """
    Get a Cover Art Archive image url from a CAA release link.
    Will return None if no Front : True exists
    """
    try:
        res = requests.get(caa_url)
        if res.status_code == 200:
            imgs = res.json().get("images", [])
            for img in imgs:
                if img.get("front"):
                    return img.get("image")
        return None

    except Exception as e:
        print(e)
        return None
    
def tag_tracks_from_info(self, album, artist, track_list):
    """
    Write to a track model's fields using internet
    search based on user-provided info.
    track_list := ["track_title1", ...,  "track_titlen"]
    """
    mbid = get_mbid_from_string(album, artist)
    if mbid:
        sleep(1)
        track_info = get_track_list_from_mbid(mbid)
        for track in track_list:
            for mb_track in track_info:
                # if there's a 75% partial match on the title, and the duration is
                # within 15 seconds, this is likely the same track
                if fuzz.partial_ratio(mb_track, track) >= 75 and \
                    abs((self.track_length - track_info[mb_track][2])) < 15:
                        
                    self.track_title = mb_track
                    self.track_number = int(track_info[mb_track][0])
                    self.disk_number = int(track_info[mb_track][1])


def get_track_list_from_mbid(mbid):
    try:
        res = requests.get(f"https://musicbrainz.org/ws/2/release/{mbid}?inc=recordings&fmt=json")
        mb_tracks = {}
        if res.status_code == 200:
            media = res.json().get("media", [])
            if media:
                for disk in range(len(media)):
                    tracks = media[disk].get("tracks", [])
                    if tracks:
                        for track in tracks:
                            title = track.get("title", None)
                            length = track.get("recording", {}).get("length", None)
                            if title:
                                track_number = track.get("number", None)
                                mb_tracks[title] = (track_number, disk+1, length)
        return mb_tracks
    
    except Exception as e:
        print(e)
        return None


