import sys

from flask import Flask, request, jsonify
from libcheckers.serialization import load_board, load_player, save_move

from ai import pick_next_move


app = Flask(__name__)


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
    app.run(port=port, debug=True)
