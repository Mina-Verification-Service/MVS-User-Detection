from flask import Flask, jsonify, request
from model import Classifier

app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def detect():
    data = request.json
    usernames = data.get('usernames')
    max_tweets = data.get('max_tweets', 5)

    usernames = usernames.split(',')
    
    if usernames == None:
        return jsonify({'error': "'usernames' parameter not found."})

    model = Classifier(usernames, max_tweets)
    predictions = model.predict()
    
    return jsonify(predictions)

if __name__ == '__main__':
    app.run(debug=True)