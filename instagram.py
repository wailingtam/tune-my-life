import urllib

from flask import Blueprint, redirect, url_for, current_app, session, jsonify, request
from flask_oauthlib.client import OAuth
import config


instagram_bp = Blueprint('instagram', __name__,
                         template_folder='templates/instagram')

oauth = OAuth(current_app)

instagram = oauth.remote_app(
    'instagram',
    consumer_key=config.INSTAGRAM_KEY,
    consumer_secret=config.INSTAGRAM_SECRET,
    request_token_params={'scope': 'basic'},
    base_url='https://api.instagram.com/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://api.instagram.com/oauth/access_token',
    authorize_url='https://api.instagram.com/oauth/authorize/'
)

token_name = 'instagram_token'


def redirect_dummy(*args, **kwargs):
    return redirect(url_for('instagram.login'))


def authenticate(f):
    def wrapper(*args, **kwargs):
        if token_name not in session:
            return redirect_dummy(*args, **kwargs)
        return f(*args, **kwargs)

    return wrapper


def insta_get(url, params=None):
    if not params:
        params = {}
    token = get_github_oauth_token()[0] or ''
    params_s = urllib.urlencode(params)

    return instagram.get(url + '?access_token=' + token +'&'+ params_s).data


# Session management views


@instagram_bp.route('/login')
def login():
    return instagram.authorize(callback=url_for('instagram.authorized', _external=True))


@instagram_bp.route('/logout')
def logout():
    session.pop(token_name, None)
    return redirect('/')


@instagram_bp.route('/login/authorized')
def authorized():
    resp = instagram.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            resp
        )
    session[token_name] = (resp['access_token'], '')
    me = insta_get('users/self/media/recent/')
    return jsonify(me)


@instagram.tokengetter
def get_github_oauth_token():
    return session.get(token_name)
