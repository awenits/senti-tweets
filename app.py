from flask import Flask, redirect, render_template, request, url_for

import helpers
import joblib

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    topic_name = request.args.get("topic_name", "").lstrip("#")
    
    if not topic_name:
        return redirect(url_for("index"))
    
    tweets = helpers.get_tweets(topic_name)
    
    ngram_vectorizer, goodSentimentClassifier = joblib.load("model.pkl") # Load "model.pkl"
    print ('Model loaded')
    
    topredict = ngram_vectorizer.transform(tweets)
    prediction = list(goodSentimentClassifier.predict(topredict))
    print(prediction)
    
    positive = prediction.count(1)
    negative = prediction.count(0)

    chart = helpers.chart(positive, negative)

    return render_template("search.html", chart=chart, topic_name=topic_name)

if __name__ == '__main__':
    app.run(port=port, debug=True)