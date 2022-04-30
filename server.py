"""
A server that responds with two pages, one showing the most recent
100 tweets for given user and the other showing the people that follow
that given user (sorted by the number of followers those users have).

For authentication purposes, the server takes a commandline argument
that indicates the file containing Twitter data in a CSV file format:

consumer_key, consumer_secret, access_token, access_token_secret
"""
import sys
from flask import Flask, render_template
from tweetie import *
from colour import Color

from numpy import median

app = Flask(__name__)

def add_color(tweets):
    """
    Given a list of tweets, one dictionary per tweet, add
    a "color" key to each tweets dictionary with a value
    containing a color graded from red to green. Pure red
    would be for -1.0 sentiment score and pure green would be for
    sentiment score 1.0.
    """
    colors = list(Color("red").range_to(Color("green"), 100))
    for t in tweets:
        score = t['score']
        # map float in (-1.0, 1.0) to int in (0, 100)
        norm_score = int(100*((score + 1)/2))
        t['color'] = colors[norm_score]

    return tweets
        


@app.route("/favicon.ico")
def favicon():
    with open('favicon_small.png', 'rb') as f:
        icon = f.read()

    return icon


@app.route("/<name>")
def tweets(name):
    "Display the tweets for a screen name color-coded by sentiment score"
    record = fetch_tweets(api, name)
    record['tweets'] = add_color(record['tweets'])
    all_scores = [t['score'] for t in record['tweets']]
    all_scores = sorted(all_scores)
    if len(all_scores) % 2:
        median = all_scores[int(len(all_scores)/2)]
    else:
        median = (all_scores[int(len(all_scores)/2) - 1] + all_scores[int(len(all_scores)/2)])/2
    return render_template('tweets.html', record=record, median=median)

@app.route("/following/<name>")
def following(name):
    """
    Display the list of users followed by a screen name, sorted in
    reverse order by the number of followers of those users.
    """
    friends_list = fetch_following(api, name)

    return render_template('following.html', name=name, friends_list=friends_list)


i = sys.argv.index('server:app')
twitter_auth_filename = sys.argv[i+1] # e.g., "/Users/parrt/Dropbox/licenses/twitter.csv"
api = authenticate(twitter_auth_filename)

#app.run(host='0.0.0.0', port=80)
