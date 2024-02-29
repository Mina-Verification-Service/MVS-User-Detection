import pickle
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/classify', methods=['POST'])
def detect():
    data = request.json

    with open('model/model.pkl', 'rb') as f:
        model = pickle.load(f)

    with open('model/vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    for d in data:
        if 'username' not in d or 'tweet' not in d:
            return jsonify({'error': "username or tweet not found."})

    tweets = [d['tweet'] for d in data]

    vector_input = vectorizer.transform(tweets)
    prediction = model.predict(vector_input)

    final_output = []

    for p in prediction:
        if p < 0.5:
            result = 'human'
        else:
            result = 'bot'

        output = {
            "result": result,
        }

        final_output.append(output)
    
    return jsonify(final_output)


if __name__ == '__main__':
    app.run(debug=True)