import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials


def get_sp_auth():  # obiekt sp z autoryzacją
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="a8b8c48cee0545c488338c72fff5779c",
                                                   client_secret="d94ae17308ef4048aa131847ce052309",
                                                   redirect_uri="https://pyrki-dashboard.herokuapp.com/",
                                                   scope="user-library-read"))
    return sp


def get_sp():  # obierkt sp bez autoryzacji
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="YOUR_APP_CLIENT_ID",
                                                               client_secret="YOUR_APP_CLIENT_SECRET"))
    return sp


if __name__ == '__main__':
    sp = get_sp_auth()
    tracks = []
    results = sp.current_user_saved_tracks(
        limit=50)  # limit = 50 to maksymalna wartość, parametr offset nie ma granicy
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(sp.audio_features(track['id']))
        print(idx, track['artists'][0]['name'], " – ", track['name'])
