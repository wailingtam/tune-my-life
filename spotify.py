import config
import spotipy
import spotipy.util as util


def get_recommendations():

    sp = spotipy.Spotify(auth=config.SPOTIFY_USER_TOKEN)
    # results = sp.search(q='artist:' + 'Arctic Monkeys', type='artist')
    results = sp.current_user()
    print results
    return True
