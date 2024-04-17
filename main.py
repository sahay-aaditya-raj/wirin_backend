from flask import Flask, jsonify, request

# Create Flask app
app = Flask(__name__)



# Define API endpoints
@app.route('/api/', methods=['POST'])
def api_test():
    print(request.get_json())
    return jsonify({"message":"received"})


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
