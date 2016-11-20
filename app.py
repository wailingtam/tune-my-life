import config
import sentiment
from feelings import average_feelings
from flask import Flask, jsonify, session, render_template
from instagram import instagram_bp, authenticate, insta_get, user_data

app = Flask(__name__)
app.config.from_object(config)


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


app.register_blueprint(instagram_bp)

if __name__ == '__main__':
    app.run()
