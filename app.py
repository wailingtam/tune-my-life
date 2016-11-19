from flask import Flask, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
import sentiment


app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)


instagram = oauth.remote_app(
    'instagram',
    consumer_key='cbd39f1ce5f54a00b68e8581753bf614',
    consumer_secret='79645a585f8940ffbd806759e1122140',
    request_token_params={'scope': 'basic'},
    base_url='https://api.instagram.com/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://api.instagram.com/oauth/access_token',
    authorize_url='https://api.instagram.com/oauth/authorize/'
)

@app.route('/')
def index():
    if 'github_token' in session:
        me = instagram.get('users/self/media/recent/')
        return jsonify(me.data)
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return instagram.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('github_token', None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    resp = instagram.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            resp
        )
    session['github_token'] = (resp['access_token'], '')
    me = instagram.get('users/self/media/recent/')
    return jsonify(me.data)


@instagram.tokengetter
def get_github_oauth_token():
    return session.get('github_token')

@app.route('/analize')
def sentimentAnalisis():
    json = sentiment.analize('https://raw.githubusercontent.com/Microsoft/ProjectOxford-ClientSDK/master/Face/Windows/Data/detection3.jpg')
    return jsonify(json)


if __name__ == '__main__':
    app.run()