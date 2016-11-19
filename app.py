import config
import sentiment
from flask import Flask, jsonify, session
from instagram import instagram_bp, authenticate, insta_get

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
if __name__ == '__main__':
    app.run()
