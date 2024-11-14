from flask import Flask,request,jsonify
from flask_cors import CORS
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer=SentimentIntensityAnalyzer()
from sklearn.feature_extraction.text import CountVectorizer
import re
from nltk.corpus import stopwords
import numpy as np

app=Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "Hello world"

@app.route("/predictComments",methods=["POST"])
def predictComments():
    data=request.get_json()
    if data and "url" in data:
        app_id=data["url"]
        num_reviews=data["noComments"]
        num_reviews=int(num_reviews)
        from google_play_scraper import reviews
        reviews_data, _ = reviews(app_id, count=num_reviews)
        df = pd.DataFrame(reviews_data)

        reviews=df['content'].tolist()


        #add any extra code here


        #Sentiment analysis
        positive=0
        negative=0
        neutral=0

        for comment in reviews:
            sentiment=analyzer.polarity_scores(comment)
            print(comment)
            print(sentiment)
            if sentiment['compound'] >= 0.05:
                positive+=1
            elif sentiment['compound'] <= -0.05:
                negative+=1
            else:
                neutral+=1



        #Keywords extraction
        stop_words = stopwords.words('english')

        def preprocess_text(text):
            processed_text = []
            for t in text:
                t = t.lower()  
                t = re.sub(r'[^\w\s]', '', t)   
                processed_text.append(t)
            return processed_text

        # Preprocess the comments
        processed_comments = preprocess_text(reviews)

        vectorizer = CountVectorizer(stop_words=stop_words, ngram_range=(1, 2)) 
        X = vectorizer.fit_transform(processed_comments)

        terms = vectorizer.get_feature_names_out()

        word_frequencies = X.toarray().sum(axis=0)

        frequency_dict = {term: word_frequencies[i] for i, term in enumerate(terms)}

        sorted_frequency = sorted(frequency_dict.items(), key=lambda x: x[1], reverse=True)

        keywords=[]

        # Display top 50 most frequent words (and bigrams)
        for term, freq in sorted_frequency[:50]:
            keywords.append(f"{term}: {int(freq)}")
            print(f"{term}: {freq}")



        response={
            "app_id":app_id,
            "Reviews":reviews,
            "Sentimental Analysis":{
                "positive":positive,
                "negative":negative,
                "neutral":neutral
            },
            "Key Words":keywords
        }

        return jsonify(response)
    return jsonify({"message": "failed"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
