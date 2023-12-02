from flask import Flask, request, jsonify
from flask_cors import CORS
from recommend import recommender

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/server', methods=['POST'])
def process_data():
    data = request.json.get('data')
    # Process the data as needed
    result = f"You entered: {data}"

    # Send additional data back to JavaScript
    additional_response = "This is an additional response from Python."

    return jsonify({'result': result, 'additionalResponse': additional_response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)