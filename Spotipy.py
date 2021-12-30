import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="a8b8c48cee0545c488338c72fff5779c",
                                               client_secret="d94ae17308ef4048aa131847ce052309",
                                               redirect_uri="https://pyrki-dashboard.herokuapp.com/",
                                               scope="user-library-read"))

results = sp.current_user_saved_tracks(limit=50) #limit = 50 to maksymalna wartość, parametr offset nie ma granicy
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name' ])