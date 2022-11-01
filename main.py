from flask import Flask, render_template, url_for, redirect, abort
from flask_bootstrap import Bootstrap4
from forms import SearchArtistForm
import requests
from dotenv import dotenv_values

env_config = dotenv_values(".env")

TOKEN_URL = 'https://api.artsy.net/api/tokens/xapp_token'
CLIENT_ID = env_config['CLIENT_ID']
CLIENT_SECRET = env_config['CLIENT_SECRET']
ARTSY_TOKEN = env_config['ARTSY_TOKEN']
REQUEST_URL = 'https://api.artsy.net/api/artists/'
HEADERS = {'X-Xapp-Token': ARTSY_TOKEN, 'Accept': 'application/vnd.artsy-v2+json'}

app = Flask(__name__)
app.config['SECRET_KEY'] = env_config['SECRET_KEY']
Bootstrap4(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/artist_search', methods=['GET', 'POST'])
def artist_search():
    form = SearchArtistForm()
    if form.validate_on_submit():
        artist_name = form.artist.data
        artist_name = artist_name.lower().replace(' ', '-')
        return redirect(url_for('artist', name=artist_name))
    return render_template('artist_search.html', form=form)


@app.route('/artist/<name>/')
def artist(name):
    url = REQUEST_URL + name
    response = requests.get(url=url, headers=HEADERS)
    data = response.json()
    try:
        links = data['_links']
    except KeyError:
        return abort(403)
    artists_request = links['similar_artists']['href']
    artworks_request = links['artworks']['href']
    artists = requests.get(url=artists_request, headers=HEADERS)
    artworks = requests.get(url=artworks_request, headers=HEADERS)
    artists = artists.json()['_embedded']['artists']
    artworks = artworks.json()['_embedded']['artworks']
    linked_artworks = [artwork for artwork in artworks if artwork['_links'].get('thumbnail')]
    return render_template('artist.html', data=data, artists=artists, artworks=linked_artworks)


if __name__ == '__main__':
    app.run(debug=True)
