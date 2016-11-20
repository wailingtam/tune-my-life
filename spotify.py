import spotipy
import datetime

def get_track_attributes(sentiment_data):
    return {}

# def get_recommendations(sentiment_data):
def get_recommendations(token):
    # attributes = get_track_attributes(sentiment_data)
    sp = spotipy.Spotify(auth=token)
    attributes = {
        'target_acousticness': 0.9,
        'target_danceability': 0,
        'target_energy': 0.1,
        'target_instrumentalness': 0.8,
        'target_liveness': 0.8,
        'target_loudness': 0.5,
        'target_speechiness': 0.2,
        'target_time_signature': 4,
        'target_valence': 0.65
    }
    results = sp.recommendations(seed_artists=[], seed_genres=['chill', 'rock', 'electronic', 'classical', 'r-n-b'], seed_tracks=[], limit=20, country=None, min_popularity=40)

    playlist_url = create_playlist(token, results)
    return playlist_url


def create_playlist(token, tracks):

    sp = spotipy.Spotify(auth=token)

    dt = datetime.datetime.now()
    creation_time = dt.strftime('%m/%d/%Y %H:%M')

    # TODO: Pass insta username
    pl = sp.user_playlist_create("tune-my-life", "usn " + creation_time, public=True)

    # Get the tracks uris
    tracks_uris = []
    for tr in tracks['tracks']:
        tracks_uris.append(tr['uri'])

    # Add tracks to the new playlist
    snapshot_id = sp.user_playlist_add_tracks("tune-my-life", pl['id'], tracks_uris)

    return pl['external_urls']['spotify']
