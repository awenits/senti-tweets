import html
import os
import plotly
import socket
import tweepy
import re


def clean_tweet(tweet):
    """Returns a cleaned tweet."""
    tweet = re.sub('http\S+\s*', '', tweet)
    tweet = re.sub('RT|cc', '', tweet)
    tweet = re.sub('#\S+', '', tweet)
    tweet = re.sub('@\S+', '', tweet)
    tweet = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), '', tweet)
    tweet = re.sub('\s+', ' ', tweet)
    return tweet


def chart(positive, negative):
    """Return a pie chart for specified sentiments as HTML."""

    figure = {
        "data": [
            {
                "labels": ["positive", "negative"],
                "hoverinfo": "none",
                "marker": {
                    "colors": [
                        "rgb(0,255,00)",
                        "rgb(255,0,0)"
                    ]
                },
                "type": "pie",
                "values": [positive, negative]
            }
        ],
        "layout": {
            "showlegend": True
            }
    }
    return plotly.offline.plot(figure, output_type="div", show_link=False, link_text=False)


def get_tweets(topic_name, count=200):
    """Return list of most recent tweets posted about topic_name."""

    # ensure count is valid
    if count < 1 or count > 200:
        raise RuntimeError("invalid count")

    cons_key = 'UHnDs4NWoFC2BqvsyTxiXZ6I1'
    cons_secret = 'vZTnAbcIxyZlt4bRBKapNWi7KGsAaCejI08a7IOCbJwGF0Q5NW'
    access_token = '766497775760576513-Eaef1z08VQMdsJ4xgxrDSIgd2SCmJpk'
    access_token_secret = 'FexRmZC1Tnpv13MH9V5IVTTfcse4Mbxizh33oUJeAYwRt'

    auth = tweepy.OAuthHandler(cons_key, cons_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    tweets = tweepy.Cursor(api.search_tweets, q=topic_name, lang="en", tweet_mode="extended").items(count)

    cleanedTweets = []
    for tweet in tweets:
        cleaned = clean_tweet(tweet.full_text)
        cleanedTweets.append(cleaned)

    return cleanedTweets
