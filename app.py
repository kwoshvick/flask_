import os
import csv
import tweepy
import datetime
import pandas as pd
from sklearn.externals import joblib
from credentials import Credentials
from cleaner import Cleaner
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from flask import Flask, redirect, url_for, request
from flask import render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    # crawler()
    user = {'username': 'Miguel222'}
    return render_template('index.html')


@app.route('/fetch', methods=['GET'])
def fetch():
    return render_template('fetch_tweet.html')


@app.route('/view', methods=['GET'])
def view():
    return render_template('view_tweets.html')


@app.route('/predict', methods=['GET'])
def predict():
    return render_template('predictions.html')


@app.route('/fetch_tweets', methods=['GET', 'POST'])
def fetch_tweets():
    if request.method == 'POST':
        print('--------------------------------------------')
        user = request.form['keywords']
        print(user)
        crawler(user)
        remove_neutral(user)
        svm_predict(user)

        # return redirect(url_for('success', name=user))
        data = prinData(user)
        return render_template('predictions.html', data=data)


def sentiment_analyzer_scores(sentence):
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(sentence)
    return score


def remove_neutral(name):
    with open('static/csv/raw/'+name+'.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        with open("static/csv/remove_neutral/remove-"+name+'.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["text"])
            for row in csv_reader:
                score = sentiment_analyzer_scores(row[0])
                if (score['compound'] >= 0.05 or score['compound'] <= -0.05):
                    writer.writerow([row[0], ])

def svm_predict(name):
    model = joblib.load('static/model/model.pkl')
    with open('static/csv/remove_neutral/remove-'+name+'.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        with open('static/csv/final/final-'+name + '.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["text", "label"])
            for row in csv_reader:
                writer.writerow([row[0], model.predict(row)[0]])


def crawler(name):
    credentials = Credentials()
    cleaner = Cleaner()
    api = credentials.authentinticate_twitter()

    today = datetime.date.today()

    print(today)
    path = "static/csv"
    print(path)
    hashtags = list()
    hashtags.append(name)
    #
    for hashtag in hashtags:
        print(hashtag)
        with open('static/csv/raw/' + hashtag + '.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["text", "label"])
            for tweet in tweepy.Cursor(api.search, q="#" + hashtag, ).items():
                writer.writerow([cleaner.clean_tweets(tweet.text), ])

    print('end')


def prinData(name):
    data1 = pd.read_csv('static/csv/final/final-' + name + '.csv')
    data = pd.DataFrame(data1)
    return data
    # print(data)
