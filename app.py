from flask import Flask, jsonify, request, Response, abort

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_root():
    response = Response('Welcome to AmbulancIA')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)