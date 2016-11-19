import config
import sentiment
from flask import Flask, jsonify, session, render_template
from instagram import instagram_bp, authenticate, insta_get
import spotify

app = Flask(__name__)
app.config.from_object(config)
user_name = 'username'


# In order to login redirect user to view instagram.login
# To logout same: instagram.logout

@app.route('/')
def index():
    user = session.get(user_name)
    return user


def get_recent_urls():
    photos = insta_get('users/self/media/recent/', params={'COUNT': 50})
    urls = [photo['images']['standard_resolution']['url'] for photo in photos['data']]
    return urls


@authenticate
@app.route('/photos/sentiments')
def photo_sentiments():
    urls = get_recent_urls()
    results = sentiment.analyze_multiple(urls)
    return jsonify(results)


app.register_blueprint(instagram_bp)

@app.route('/get-playlist')
def get_playlist():
    spotify.get_recommendations()
    return render_template("main.html")


if __name__ == '__main__':
    app.run()
