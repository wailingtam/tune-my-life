import config
from flask import Flask, jsonify, render_template, request, redirect, session
import sentiment
from instagram import instagram_bp, authenticate, insta_get, user_data
import spotify
import base64
import requests
import urllib
import json

app = Flask(__name__)
app.config.from_object(config)

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": config.SPOTIFY_CLIENT_ID
}


# In order to login redirect user to view instagram.login
# To logout same: instagram.logout

@app.route('/')
def index():
    user = session.get(user_data)

    if user is None:
        images = [{'caption': 'Amasd', 'url': 'http://i.imgur.com/uL6IFOW.jpg'},
                  {'caption': 'asda', 'url': 'http://i.imgur.com/W5YdAgM.jpg'}]
    else:
        images = get_recent_photos()

    return render_template('index.html', images=images, logged_in=(user is not None))


@app.route('/get-auth')
def get_authorization():
    url_args = "&".join(["{}={}".format(key, urllib.quote(val)) for key, val in auth_query_parameters.iteritems()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


def get_recent_urls():
    photos = insta_get('users/self/media/recent/', params={'COUNT': 50})
    urls = [photo['images']['standard_resolution']['url'] for photo in photos['data']]
    return urls


def get_recent_photos():
    photos = insta_get('users/self/media/recent/', params={'COUNT': 50})
    urls = [{
                'url': photo['images']['standard_resolution']['url'],
                'caption': photo['caption']['text'] if photo['caption'] else ' '
            }
            for photo in photos['data']]
    return urls


def average_feelings(sublist):
    if not sublist:
        return None
    t_score = {
        'anger': 0,
        'contempt': 0,
        'disgust': 0,
        'fear': 0,
        'happiness': 0,
        'neutral': 0,
        'sadness': 0,
        'surprise': 0,
    }
    for item in sublist:
        if 'scores' in item:
            for k, v in item['scores'].items():
                t_score[k] += v
    length = len(sublist)
    f_score = map(lambda (k, v): (k, v / length), t_score.items())
    return dict(f_score)


@authenticate
@app.route('/photos/sentiments')
def photo_sentiments():
    urls = get_recent_urls()
    photos = sentiment.analyze_multiple(urls)
    faces = [average_feelings(sublist) for sublist in photos]
    return jsonify(faces)


app.register_blueprint(instagram_bp)


@app.route('/get-playlist')
def get_playlist(token):
    spotify.get_recommendations(token)
    return render_template("main.html")


@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": config.SPOTIFY_REDIRECT_URI
    }
    base64encoded = base64.b64encode("{}:{}".format(config.SPOTIFY_CLIENT_ID, config.SPOTIFY_CLIENT_SECRET))
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    # refresh_token = response_data["refresh_token"]
    # token_type = response_data["token_type"]
    # expires_in = response_data["expires_in"]
    playlist_url = spotify.get_recommendations(access_token)
    return playlist_url

if __name__ == '__main__':
    app.run()
