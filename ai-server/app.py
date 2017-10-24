import sys
import time

from flask import Flask, g, request, jsonify
from libcheckers.serialization import load_board, load_player, save_move

from ai import pick_next_move


app = Flask(__name__)


@app.before_request
def before_request():
    g.request_start_time = time.time()


@app.teardown_request
def teardown_request(exception=None):
    request_serving_time = time.time() - g.request_start_time
    with open('request-timing.csv', 'a') as rtf:
        rtf.write('{0:.5f}\n'.format(request_serving_time))


@app.route('/move', methods=['POST'])
def move():
    payload = request.get_json()

    try:
        board = load_board(payload['board'])
        player = load_player(payload['playerTurn'])
    except:
        return jsonify({'message': 'Invalid request payload'}), 422

    move_obj = pick_next_move(board, player)
    move_payload = save_move(move_obj)
    return jsonify(move_payload)


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(port=port)
