from flask import Flask,request,jsonify
from flask_cors import CORS
import pandas as pd

app=Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

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

        



        response={
            "app_id":app_id,
            "Reviews":reviews,
        }

        return jsonify(response)
    return jsonify({"message": "failed"})

if __name__=="__main__":
    app.run(debug=True)