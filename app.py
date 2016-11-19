import config
import sentiment
import spotify
from flask import Flask, jsonify, session, render_template
from instagram import instagram_bp, authenticate, insta_get, user_data

app = Flask(__name__)
app.config.from_object(config)


# In order to login redirect user to view instagram.login
# To logout same: instagram.logout

@app.route('/')
def index():
    user = session.get(user_data)

    if user:
        imageurls = get_recent_urls()
    else:
        imageurls = ['http://i.imgur.com/uL6IFOW.jpg', 'http://i.imgur.com/W5YdAgM.jpg']

    return render_template('index.html', imageurls=imageurls)


def get_recent_urls():
    photos = insta_get('users/self/media/recent/', params={'COUNT': 50})
    urls = [photo['images']['standard_resolution']['url'] for photo in photos['data']]
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
def get_playlist():
    spotify.get_recommendations()
    return render_template("index.html")


@app.route('/home')
def home():
    imageurls = ['http://i.imgur.com/uL6IFOW.jpg', 'http://i.imgur.com/W5YdAgM.jpg']
    return render_template('index.html', imageurls=imageurls)


if __name__ == '__main__':
    app.run()
