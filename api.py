import spotipy, sys, os
import spotipy.util as util

SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'

def get_access_token(username):
    """Return access token from Spotify for defined scopes."""

    scope = 'user-library-read'

    # Get access token from Spotify authorization server.
    token = util.prompt_for_user_token(username, scope, 
                                    client_id = SPOTIPY_CLIENT_ID, 
                                    client_secret = SPOTIPY_CLIENT_SECRET, 
                                    redirect_uri = SPOTIPY_REDIRECT_URI)

    if token:
        # sp = spotipy.Spotify(auth=token)
        return token  
    else:
        return None


def get_playlist_tracks(user_id, token, playlist_list=['5vt2cOxZrcn9yVzTTIURJe', '4xP6FbKJ28lbo9JSqJ9MbZ']):
    """Print all the tracks in a playlist."""

    sp = spotipy.Spotify(auth=token)
    compiled_playlist_tracks = {}

    for playlist_id in playlist_list:
        # Get all tracks of a playlist.
        results = sp.user_playlist_tracks(user_id, playlist_id)
        compiled_playlist_tracks[playlist_id] = []
        playlist_tracks = results['items']

        # If number of tracks exceeds the limit,
        # continue getting the next set until all tracks are retrieved.
        while results['next']:
            results = sp.next(results)
            playlist_tracks.extend(results['items'])
        
        # Add to dictionary where key = playlist_id and value = list of tracks
        for item in playlist_tracks:
            track = item['track']
            compiled_playlist_tracks[playlist_id].append(track['id'])

    return compiled_playlist_tracks


def get_playlists(user_id, token):
    """Print all user playlists."""

    sp = spotipy.Spotify(auth=token)

    # Get user playlists
    results = sp.user_playlists(user_id)
    playlists = results['items']

    # Number of playlists retrieved in inital call is limited.
    # If the user has more playlists than the limit, retrieve the remaining.
    while results['next']:
        results = sp.next(results)
        playlists.extend(results['items'])
    
    return playlists


def get_track_audio_features(token, track_list=['0Brf1s65f8eekORKK9gpe4', '3hYdai5p5sQ3vAmHQ6uaK6']):
    """Print audio features of a track."""

    sp = spotipy.Spotify(auth=token)

    # Audio_features function returns a list of dictionaries.
    track_fts = sp.audio_features(track_list)
    print(track_fts)
    return track_fts

    # for track in track_fts:
    #     #General info of track
    #     track_id = track['id']
    #     track_general_info = self.sp.track(track_id)
    #     name = track_general_info['name']
    #     # artist = 
    #     user_id = self.username
    #     # playlist_id = 

    #     # Track features
    #     key = track['key']
    #     mode = track['mode']
    #     danceability = track['danceability']
    #     energy = track['energy']
    #     instrumentalness = track['instrumentalness']
    #     loudness = track['loudness']
    #     speechiness = track['speechiness']
    #     valence = track['valence']   
    #     tempo = track['tempo']   
    #     uri = track['uri']   
    #     href = track['track_href']   
    #     duration = track['duration_ms'] 
    #     print(f"key: {key}, mode: {mode}, energy: {energy}, tempo: {tempo}, uri: {uri}")   

def get_track_general_info(token, track_id):
    """Return the general info of a track."""

    sp = spotipy.Spotify(auth=token)
    track_general_info = sp.track(track_id)

    return track_general_info