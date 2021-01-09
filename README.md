# playlist_generator
This is a script that generates a Spotify playlist from a text file.

## APIs
- [Spotify web api](https://developer.spotify.com/documentation/web-api/)
- [Python requests library](https://requests.readthedocs.io/en/master/)

## Setup
1. Install dependencies
```pip3 install -r requirements.txt```

2. Collect your Spotify user ID and OAuth token From Spotify and add it to an .env file
- to get your user ID, click [here](https://www.spotify.com/us/account/overview/) and copy your username
- to get your OAuth token, click [this link](https://developer.spotify.com/console/post-playlists/) and then click the `Get Token` button
  > Note: this token expires in one hour, so you will have to refresh it each time

3. Run the `create_playlist.py` file
```python3 create_playlist.py```
