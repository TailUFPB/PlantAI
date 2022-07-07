from flask import Flask, jsonify, request, Response, abort
from src.agent import Agent

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_root():
    response = Response('Welcome to PlantAI')
    return response

@app.route('/decide_action', methods=['POST'])
def decide_action():
    request_data = request.get_json()

    state = request_data.get("state")
    action = Agent.decide_action(state)

    return jsonify(action)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)