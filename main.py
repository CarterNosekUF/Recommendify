from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from recommend import recommender

app = Flask(__name__, static_folder="./static")
CORS(app)  # Enable CORS for all routes


@app.route('/server', methods=['POST'])
def process_data():
    link = request.json.get('data')
    sort = request.json.get('sort_method')
    recommendation = recommender(link, sort)
    result = recommendation.get_recommendations()

    return jsonify({'recommendations': result})


@app.route('/', methods=["GET"])
def index():
    return send_file('./index.html')


if __name__ == '__main__':
    app.run(port=5500)
