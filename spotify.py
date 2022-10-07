import random

import requests
import configparser
import base64
from lyricsgenius import Genius
from trivia import translate

config = configparser.ConfigParser()
config.read('config.ini')

client_id = config['SPOTIFY']['client_id']
client_secret = config['SPOTIFY']['client_secret']
genius_client_id = config['GENIUS_LYRICS']['client_id']
genius_client_secret = config['GENIUS_LYRICS']['client_secret']
genius = Genius(config['GENIUS_LYRICS']['client_access_token'])

reqSession = requests.Session()


def getToken():
    url = 'https://accounts.spotify.com/api/token'

    autorisation_headers = {
        'Authorization': 'Basic ' + base64.b64encode(bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    token = reqSession.post(url, headers=autorisation_headers, data={'grant_type': 'client_credentials'}).json()
    return token['access_token']


def getApiHeader():
    return {
        'Authorization': 'Bearer ' + getToken()
    }


def getInfoTrack(track_name):
    track_id = getTrackID(track_name)
    params = {'market': 'FR'}
    url = 'https://api.spotify.com/v1/tracks/' + track_id
    return reqSession.get(url, headers=getApiHeader(), params=params).json()


def getTrackID(track_name):
    print(track_name)
    params = {'q': track_name, 'type': 'track', 'market': 'FR'}
    url = 'https://api.spotify.com/v1/search'
    tracks = reqSession.get(url, headers=getApiHeader(), params=params).json()
    if tracks['tracks']['total'] == 0:
        return None
    return tracks['tracks']['items'][0]['id']


# song = genius.search_song("Lose Yourself",get_full_info=False)
# song = genius.lyrics(song_id=(song.to_dict()['id']),remove_section_headers=True,)


def getLyrics(track, artist):
    song = genius.search_song(track, artist, get_full_info=False)
    if song is None:
        return None
    song= genius.lyrics(song_id=(song.to_dict()['id']), remove_section_headers=True)
    lyrics = song
    lyrics = lyrics.split('\n')
    lyrics = [line for line in lyrics if line != '']
    lyrics.pop(0)
    lyrics.pop(-1)
    x=len(lyrics)
    ligne = random.randint(0, x-6)
    lyrics = lyrics[ligne:ligne+4]
    lyrics = '\n'.join(lyrics)
    return lyrics


def getArtistId(artist):
    params = {'q': artist, 'type': 'artist', 'market': 'FR'}
    url = 'https://api.spotify.com/v1/search'
    artists = reqSession.get(url, headers=getApiHeader(), params=params).json()
    if artists['artists']['total'] == 0:
        return None
    return artists['artists']['items'][0]['id']


def getInfoArtist(artist):
    artist_id = getArtistId(artist)
    params = {'market': 'FR'}
    url = 'https://api.spotify.com/v1/artists/' + artist_id
    return reqSession.get(url, headers=getApiHeader(), params=params).json()


def getAlbums(artist):
    artist_id = getArtistId(artist)
    params = {'market': 'FR', 'include_groups': 'album,single'}
    url = 'https://api.spotify.com/v1/artists/' + artist_id + '/albums'
    reponse = reqSession.get(url, headers=getApiHeader(), params=params).json()
    albums = []
    for album in reponse['items']:
        albums.append(album['id'])
    return albums


def getAlbumsTracks(artist):
    tracks = []
    albums = getAlbums(artist)
    for album in albums:
        params = {'market': 'FR'}
        url = 'https://api.spotify.com/v1/albums/' + album + '/tracks'
        reponse = reqSession.get(url, headers=getApiHeader(), params=params).json()
        for track in reponse['items']:
            tracks.append(track['name'])
        tracks = list(set(tracks))
    return tracks


# print(getLyrics(song))
# print(song.lyrics)
def randomLyrics(artist):
    tracks = getAlbumsTracks(artist)
    track = random.choice(tracks)
    lyrics = getLyrics(track, artist)
    if lyrics is None:
        return randomLyrics(artist)
    return lyrics, track

def translatedLyrics(artist, lang):
    tracks = getAlbumsTracks(artist)
    track = random.choice(tracks)
    lyrics = getLyrics(track, artist)
    if lyrics is None:
        return randomLyrics(artist)
    lyrics = translate(lyrics, lang)
    return lyrics, track


