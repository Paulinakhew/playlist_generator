'''
Step 1: Create a new playlist on Spotify.
'''
import json
import requests
import os
from dotenv import load_dotenv
from exceptions import ResponseException

load_dotenv()
spotify_token = os.environ.get("SPOTIFY_TOKEN")
spotify_user_id = os.environ.get("SPOTIFY_USER_ID")

class CreatePlaylist:
    def __init__(self):
        self.user_id = spotify_user_id
        self.songs = {}

    def create_playlist(self):
        '''Create a new playlist on Spotify'''
        request_body = json.dumps({
            "name": "New Playlist",
            "description": "New playlist for songs",
            "public": True
        })

        query = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type":"application/json",
                "Authorization":f"Bearer {spotify_token}"
            }
        )
        response_json = response.json()

        # playlist id
        return response_json["id"]

    def get_spotify_uri(self, song_name, artist):
        '''Search for a song on Spotify'''
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {spotify_token}"
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]

        # only use the first song
        uri = songs[0]["uri"]

        return uri

    def get_song_names(self):
        song_data = open('song_list.txt', 'r')
        lines = song_data.readlines()

        songs = {}
        for line in lines:
            line = line.split("-", 1)[1].strip().split(" by ")
            song_name = line[0]
            artist = line[1]

            if song_name is not None and artist is not None:
                # save all important info and skip any missing song and artist
                self.songs[song_name] = {
                    "artist": artist,
                    "song_name": song_name,

                    # add the uri, easy to get song to put into playlist
                    "spotify_uri": self.get_spotify_uri(song_name, artist)
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
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )

        # check for valid response status
        if response.status_code != 201:
            raise ResponseException(response.status_code)

        response_json = response.json()
        return response_json


if __name__ == "__main__":
    cp = CreatePlaylist()
    cp.add_song_to_playlist()
