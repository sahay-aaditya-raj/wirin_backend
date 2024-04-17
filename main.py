from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS from flask_cors

app = Flask(__name__)
CORS(app)  # Apply CORS to your Flask app

# Sample endpoint to receive POST requests
@app.route('/', methods=['POST'])
def receive_data():
    data = request.get_json()
    print("Received Data:", data)
    return jsonify({"message": "Data received successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
