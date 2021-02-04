'''
Step 1: Create a new playlist on Spotify.
'''
import json
import requests
import os

from exceptions import ResponseException


class CreatePlaylist:
    def __init__(self):
        self.user_id = None
        self.spotify_token = None
        self.songs = {}

    def set_credentials(self, user_id, spotify_token):
        self.user_id = user_id
        self.spotify_token = spotify_token

    def create_playlist(self, playlist_name:str, playlist_description:str, public_playlist:bool):
        '''Create a new playlist on Spotify'''
        playlist_name = playlist_name if playlist_name else "New Playlist"
        playlist_description = playlist_description if playlist_description else "New playlist for songs"
        request_body = json.dumps({
            "name": playlist_name,
            "description": playlist_description,
            "public": public_playlist
        })

        query = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type":"application/json",
                "Authorization":f"Bearer {self.spotify_token}"
            }
        )
        response_json = response.json()

        if 'id' not in response_json:
            raise Exception("Invalid token and username")

        # playlist id
        return response_json["id"]

    def get_spotify_uri(self, song_name, artist):
        '''Search for a song on Spotify'''
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )

        try:
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.spotify_token}"
                }
            )

            response_json = response.json()
            songs = response_json["tracks"]["items"]

            # only use the first song
            uri = songs[0]["uri"]

            return uri
        except Exception:
            return

    def get_song_names(self):
        song_data = open('song_list.txt', 'r')
        lines = song_data.readlines()

        songs = {}
        for line in lines:
            line = line.strip().split(" ", 1)[1].strip().split(" - ")
            artist = line[0]
            song_name = line[1]

            # skip missing song or artist
            if song_name is not None and artist is not None:
                # skip song with missing uri
                spotify_uri = self.get_spotify_uri(song_name, artist)
                if spotify_uri:
                    self.songs[song_name] = {
                        "artist": artist,
                        "song_name": song_name,
                        "spotify_uri": spotify_uri
                    }

    def add_song_to_playlist(self):
        # get songs into songs dictionary
        self.get_song_names()

        # collect all of uri
        uris = [info["spotify_uri"]
                for song, info in self.songs.items()]

        # create a new playlist
        playlist_id = self.create_playlist()

        # add all songs into new playlist
        request_data = json.dumps(uris)

        query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )

        response_json = response.json()
        return response_json

    def get_submitted_song_names(self, submitted_songs: str, timestamp_del:str, artist_song_del:str, artist_song:bool):
        lines = submitted_songs.splitlines()

        for line in lines:
            if timestamp_del:
                line = line.strip().split(timestamp_del, 1)[1].strip()

            line = line.split(artist_song_del)

            if artist_song:
                artist = line[0].strip()
                song_name = line[1].strip()
            else:
                artist = line[1].strip()
                song_name = line[0].strip()

            # skip missing song or artist
            if song_name is not None and artist is not None:
                # skip song with missing uri
                spotify_uri = self.get_spotify_uri(song_name, artist)
                if spotify_uri:
                    self.songs[song_name] = {
                        "artist": artist,
                        "song_name": song_name,
                        "spotify_uri": spotify_uri
                    }

    def add_submitted_songs_to_playlist(
        self,
        submitted_songs:str,
        del1:str,
        del2:str,
        playlist_name:str,
        playlist_description:str,
        artist_song:bool,
        public_playlist:bool
    ):
        # get songs into songs dictionary
        self.get_submitted_song_names(submitted_songs, del1, del2, artist_song)

        # collect all of uri
        uris = [info["spotify_uri"]
                for song, info in self.songs.items()]

        # create a new playlist
        playlist_id = self.create_playlist(playlist_name, playlist_description, public_playlist)

        # add all songs into new playlist
        request_data = json.dumps(uris)

        query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )

        response_json = response.json()
        return response_json
