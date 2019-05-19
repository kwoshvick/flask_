from predict import write
from search_tweets import search_tweets
from stream_tweets import track
from read_tweets import read_tweets, read_results
from flask import render_template, request
from app import app

from .forms import TweetsForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/collect_tweets')  # loads search tweets html template
def collect_tweets():
    return render_template('tweets.html')


@app.route('/stream_tweets')
def stream():
    return render_template('stream_tweets.html')


@app.route('/stream_tweets', methods=['POST'])  # loads streaming tweets html template
def stream_tweets():
    keywords = request.form['keywords']
    track(keywords)

    return "true"


@app.route('/final_tweets', methods=['POST'])
def final():
    keywords = request.form['keywords']
    search_tweets(keywords)

    return view_tweets()


@app.route('/view_tweets')
def view_tweets():
    items = read_tweets()

    return render_template('view_tweets.html', items=items)


@app.route('/predicted')
def predicted():
    write()

    return results()


@app.route('/results')
def results():
    items = read_results()

    return render_template("predicted.html", items=items)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'