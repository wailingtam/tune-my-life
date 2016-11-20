import config
from flask import Flask, jsonify, render_template, request, redirect, session
import sentiment
import spotify
from feelings import average_feelings
from flask import Flask, jsonify, session, render_template
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

    return render_template('index.html', images=images, user=user)


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


@authenticate
@app.route('/photos/sentiments')
def photo_sentiments():
    urls = get_recent_urls()
    photos = sentiment.analyze_multiple(urls)
    faces = [average_feelings(sublist) for sublist in photos]
    return jsonify(faces)


@authenticate
@app.route('/playlist')
def playlist():
    return jsonify({'playlist_url':'http://gerard.space'})

app.register_blueprint(instagram_bp)

if __name__ == '__main__':
    app.run()
