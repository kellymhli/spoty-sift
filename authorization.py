import spotipy, sys, os
import spotipy.util as util

SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'

def get_access_token(username):
    """Return access token from Spotify for defined scopes."""

    scope = 'user-library-read'

    # Get access token from Spotify authorization server
    token = util.prompt_for_user_token(username, scope, 
                                       client_id = SPOTIPY_CLIENT_ID, 
                                       client_secret = SPOTIPY_CLIENT_SECRET, 
                                       redirect_uri = SPOTIPY_REDIRECT_URI)

    if token:
        return token 
    else:
        return None


def get_playlist_tracks(username, sp, playlist_id='5vt2cOxZrcn9yVzTTIURJe'):
    """Print all the tracks in a playlist."""

    results = sp.user_playlist_tracks(username, playlist_id)
    playlist_tracks = results['items']
    while results['next']:
        results = sp.next(results)
        playlist_tracks.extend(results['items'])

    for item in playlist_tracks:
        track = item['track']
        print(f"{playlist_id}|||{track['id']}")
        
    # Tracks of user's saved songs list (songs not in a playlist) 
    # results = sp.current_user_saved_tracks()
    # playlist_tracks = results['items']
    # while results['next']:
        # results = sp.next(results)
        # playlist_tracks.extend(results['items'])


def get_playlists(username, sp):
    """Print all user playlists."""

    results = sp.user_playlists(username)
    playlists = results['items']
    while results['next']:
        results = sp.next(results)
        playlists.extend(results['items'])

    for playlist in playlists:
        if playlist['owner']['id'] == username:
            print(f"{playlist['id']}|||{playlist['name']}|||{playlist['owner']['id']}")


def get_track_audio_features(username, sp, track_list=['0Brf1s65f8eekORKK9gpe4']):
    """Print audio features of a track."""

    # Audio_features funtion returns a list of dictionaries
    track_fts = sp.audio_features(track_list)
    for track in track_fts:
        #General info of track
        track_id = track['id']
        track_general_info = sp.track(track_id)
        name = track_general_info['name']
        # artist
        user_id = username
        # playlist_id

        # Track features
        key = track['key']
        mode = track['mode']
        danceability = track['danceability']
        energy = track['energy']
        instrumentalness = track['instrumentalness']
        loudness = track['loudness']
        speechiness = track['speechiness']
        valence = track['valence']   
        tempo = track['tempo']   
        uri = track['uri']   
        href = track['track_href']   
        duration = track['duration_ms'] 
        print(f"key: {key}, mode: {mode}, energy: {energy}, tempo: {tempo}, uri: {uri}")   


def authorize(username):
    """Instantiate Spotify object for user using given username."""

    token = get_access_token(username)
    sp = spotipy.Spotify(auth=token)
    
    get_playlists(username, sp)
    get_playlist_tracks(username, sp)
    get_track_audio_features(username, sp)
