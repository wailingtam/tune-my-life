import config
import sentiment
from flask import Flask, jsonify, session, render_template
from instagram import instagram_bp, authenticate, insta_get, user_data
import spotify

app = Flask(__name__)
app.config.from_object(config)


# In order to login redirect user to view instagram.login
# To logout same: instagram.logout

@app.route('/')
def index():
    user = session.get(user_data)
    return jsonify(user) or 'NO USER'


def get_recent_urls():
    photos = insta_get('users/self/media/recent/', params={'COUNT': 50})
    urls = [photo['images']['standard_resolution']['url'] for photo in photos['data']]
    return urls


def average_feelings(sublist):
    # for item in sublist:
    #     if 'score' in item:
    #
    # map(lambda x: x['score'])
    pass

@authenticate
@app.route('/photos/sentiments')
def photo_sentiments():
    urls = get_recent_urls()
    photos = sentiment.analyze_multiple(urls)
    faces = [average_feelings(sublist) for sublist in photos]
    songs = spotify.get
    return jsonify(faces)


app.register_blueprint(instagram_bp)

@app.route('/get-playlist')
def get_playlist():
    spotify.get_recommendations()
    return render_template("index.html")


@app.route('/')
def home():
    imageurls = ['http://i.imgur.com/uL6IFOW.jpg', 'http://i.imgur.com/W5YdAgM.jpg']
    return render_template('index.html', imageurls=imageurls)

if __name__ == '__main__':
    app.run()
