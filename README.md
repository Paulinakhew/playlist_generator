# playlist_generator
This is a script that generates a Spotify playlist from a text file.

## Tools and APIs
- [Spotify web api](https://developer.spotify.com/documentation/web-api/)
- [Python requests library](https://requests.readthedocs.io/en/master/)

## Nice to know
- Learn about OAuth for free [here](https://www.oauth.com/oauth2-servers/background/). I've created a repo that implements a simple OAuth script using python and the GitHub API [here](https://github.com/Paulinakhew/oauth).

## Setup
1. Install dependencies

```pip3 install -r requirements.txt```

2. Collect your Spotify user ID and OAuth token From Spotify and add it to an `.env` file
- to get your user ID, click [here](https://www.spotify.com/us/account/overview/) and copy your username
- to get your OAuth token, click [this link](https://developer.spotify.com/console/post-playlists/) and then click the `Get Token` button
  > Note: this token expires in one hour, so you will have to refresh it each time

Your `.env` file should be formatted as follows:

```
CLIENT_ID=
CLIENT_SECRET=
REDIRECT_URI=http://127.0.0.1:5000/callback
SECRET_KEY= #Use output of python -c 'import os; print(os.urandom(16))'
```

3. Run the `create_playlist.py` file

```python3 flask_app.py```

## How it works
![First page](static/1.png?raw=true "First page")
The first page has a button that triggers the Spotify authentication flow.

![Second page](static/2.png?raw=true "Second page")
If you're not logged in on the web browser, you'll be taken to the second page where you can log in through the method of your choice.

![Third page](static/3.png?raw=true "Third page")
Once you've been logged in, you'll need to copy the two fields at the top and paste them into the first two textboxes. Once that has been complete, you can paste a list of songs into the large textbox and paste the delimiters.

## Example
### List of Songs
The `List of songs` field would be populated by a list of songs. The following example is taken from a comment from [this](https://www.youtube.com/watch?v=r3X2Y-Xuwwo&ab_channel=honimilk) YouTube video.
```
0:02 - Butterfly by UMI
2:43 - Chateau by Djo
7:16 - Six AM by Inner Wave
9:23 - In a Mood by TheSecondSex
13:31 - Lavender Kiss by The Licks
17:35 - Gimme Love by Joji
21:11 - Sink Into the Floor by Feng Suave
25:49 - Somebody Else by The 1975
31:39 - Only in my Dreams by The Marías
34:30 - Love it if We Made it by The 1975
38:43 - Freakin' Out On the Interstate by Briston Maroney
42:56 - Midnight Blue by Puma Blue
47:36 - Loverboy by The Marías
51:26 - Soft Porn by Puma Blue
```
As you can see, the YouTube timestamps have been included. To get rid of these, you would fill out the first delimiter field.

### First delimiter
This field is where you would place the symbol/text that separates the timestamps from the rest of the information. In this case, it is a dash.
```
-
```
The code will remove everything located up until the `-`, leaving the text on the right side.

### Second delimiter
This field is where you would place the symbol/text that separates the artist name from the song name.
```
by
```
The code will separate the artist and songs by the second delimiter (which is `by` in this case). It will use the Spotify API to search up each song by artist and song name and add it to a public playlist.

### Playlist name (optional)
If you want to create a custom playlist name, you would add that here. Otherwise, the default is `New Playlist`
```
Songs to listen to on a late night drive
```

### Playlist description (optional)
If you want to add a custom playlist description, you would add that here. Otherwise, the default is `New playlist for songs`
```
Playlist generated from a YouTube video
```

### order: artist -> song
Check off this checkbox if the artist is placed before the song names. Otherwise, leave it blank.

### Success!!
If the playlist was successfully created, you will see a green alert box pop up with the response from Spotify. This will contain a `snapshot_id`. Your new playlist should appear immediately on Spotify.
![Success](static/success.png?raw=true "Success")
