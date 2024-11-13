from flask import Flask,request,jsonify
from flask_cors import CORS

app=Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route("/")
def index():
    return "Hello world"

@app.route("/predictComments",methods=["POST"])
def predictComments():
    data=request.get_json()
    if data and "url" in data:
        base_url=data["url"]
        no_comments=data["noComments"]

        response={
            "url":base_url,
            "No of Comments":no_comments
        }

        return jsonify(response)
    return jsonify({"message": "failed"})

if __name__=="__main__":
    app.run(debug=True)