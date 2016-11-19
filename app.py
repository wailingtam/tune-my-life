import sentiment
from flask import Flask, jsonify
from instagram import instagram_bp, authenticate, insta_get
import config

app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(instagram_bp)


@authenticate
@app.route('/photos/urls')
def index():
    return jsonify(get_recent_urls())


def get_recent_urls():
    photos = insta_get('users/self/media/recent/', params={'COUNT': 50})
    urls = [photo['images']['standard_resolution']['url'] for photo in photos['data']]
    return urls


@app.route('/analize')
def sentimentAnalisis():
    json = sentiment.analize(
        'https://raw.githubusercontent.com/Microsoft/ProjectOxford-ClientSDK/master/Face/Windows/Data/detection3.jpg')
    return jsonify(json)


if __name__ == '__main__':
    app.run()
