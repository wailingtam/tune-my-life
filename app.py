import config
from flask import Flask, jsonify, render_template, request, redirect, session
import sentiment
import spotify
from feelings import average_feelings
from flask import Flask, jsonify, session, render_template
from instagram import instagram_bp, authenticate, insta_get, user_data, token_name
from spotify import spotify_bp,spotify_at
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

    return render_template('index.html', images=images, user=user)


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

app.register_blueprint(spotify_bp)

@app.route('/logout')
def logout():
    session.pop(token_name, None)
    session.pop(user_data, None)
    session.pop(spotify_at, None)
    return redirect('/')


if __name__ == '__main__':
    app.run()
