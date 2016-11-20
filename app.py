import config
from flask import Flask, jsonify, render_template, request, redirect, session
import sentiment
import spotify
from feelings import average_feelings, to_music
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
        images = [{'title':'', 'caption': '', 'url': 'https://images.pexels.com/photos/27411/pexels-photo-27411.jpg?w=1260&h=750&auto=compress&cs=tinysrgb'},
                  {'title':'Do you', 'caption': '', 'url':'http://i.imgur.com/W5YdAgM.jpg'},
                  {'title':'want to get', 'caption': '', 'url':'http://i.imgur.com/7AwG6iO.jpg'},
                  {'title':'', 'caption': '', 'url':'http://how-old.net/Images/faces2/scroll005.jpg'},
                  {'title':'the playlist', 'caption': '', 'url':'https://images.pexels.com/photos/798/bench-people-smartphone-sun.jpg?w=1260&h=750&auto=compress&cs=tinysrgb'},
                  {'title':'of', 'caption': '', 'url':'https://images.pexels.com/photos/108048/pexels-photo-108048.jpeg?w=1260&h=750&auto=compress&cs=tinysrgb'},
                  {'title':'your', 'caption': '', 'url':'http://i.imgur.com/AmsU4OV.jpg'},
                  {'title':'life?', 'caption': '', 'url':'https://images.pexels.com/photos/5929/food-salad-dinner-eating.jpg?w=1260&h=750&auto=compress&cs=tinysrgb'}]
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
                'caption': photo['caption']['text'] if photo['caption'] else ' ',
                'title': ''
            }
            for photo in photos['data']]
    return urls


@authenticate
@app.route('/playlist')
def photo_sentiments():
    urls = get_recent_urls()
    photos = sentiment.analyze_multiple(urls)
    inputs = [to_music(average_feelings(sublist)) for sublist in photos]
    playlist_url = spotify.get_recommendations(inputs)
    return jsonify({'playlist_url':playlist_url})



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
