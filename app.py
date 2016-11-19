from flask import Flask, jsonify
from instagram import instagram_bp, authenticate, insta_get

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
app.register_blueprint(instagram_bp)


@authenticate
@app.route('/photos/urls')
def index():
    photos = insta_get('users/self/media/recent/', params={'COUNT': 50})
    urls =  [photo['images']['standard_resolution']['url'] for photo in photos['data']]
    return jsonify(urls)


if __name__ == '__main__':
    app.run()
