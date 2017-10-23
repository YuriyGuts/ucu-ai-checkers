#!/usr/bin/env python3

import logging
import random
import sys
from urllib.parse import urljoin

import requests
from libcheckers.enum import Player, PieceClass, GameOverReason
from libcheckers.movement import Board
from libcheckers.serialization import load_move, save_board, save_player


log_format = '%(asctime)s | %(levelname)8s | %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=log_format)
logger = logging.getLogger(__name__)


MAX_MOVES = 100


def run_arena(white_server_url, black_server_url):
    board = get_starting_board()

    for move_number in range(1, MAX_MOVES + 1):
        # White move.
        game_over = board.check_game_over(Player.WHITE)
        if game_over:
            logger.info('Game over: {0}'.format(get_reason_message(game_over)))
            return
        white_move = get_player_move(move_number, board, Player.WHITE, white_server_url)
        board = white_move.apply(board)

        # Black move.
        game_over = board.check_game_over(Player.BLACK)
        if game_over:
            logger.info('Game over: {0}'.format(get_reason_message(game_over)))
            return
        black_move = get_player_move(move_number, board, Player.BLACK, black_server_url)
        board = black_move.apply(board)

    logger.info('Game over: maximum limit of moves reached')


def get_starting_board():
    board = Board()
    for index in range(31, 51):
        board.add_piece(index, Player.WHITE, PieceClass.MAN)
    for index in range(1, 21):
        board.add_piece(index, Player.BLACK, PieceClass.MAN)
    return board


def get_player_move(move_num, board, player, server_url):
    player_name = save_player(player)
    allowed_moves = board.get_available_moves(player)

    payload = {
        'board': save_board(board),
        'playerTurn': player_name,
    }
    url = urljoin(server_url, 'move')
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        msg = 'Player {0}: server has responded with an unexpected status code: {1} ({2})'
        logger.warning(msg.format(player_name, response.status_code, response.content))

    try:
        move = load_move(response.json())
    except:
        msg = 'Player {0}: Unable to parse the move returned by the server ({1}). Picking a random move instead'
        logger.warning(msg.format(player_name, response.content))
        move = random.choice(allowed_moves)

    if move not in allowed_moves:
        msg = 'Player {0} picked a move that is not allowed ({1}). Picking a random move instead'
        logger.warning(msg)
        move = random.choice(allowed_moves)

    logger.info('Move {0:3d}: {1} plays {2}'.format(move_num, player_name, move))
    return move


def get_reason_message(game_over_reason):
    if game_over_reason == GameOverReason.WHITE_WON:
        return 'white won'
    elif game_over_reason == GameOverReason.BLACK_WON:
        return 'black won'
    elif game_over_reason == GameOverReason.DRAW:
        return 'draw'


def main():
    if len(sys.argv) != 3:
        print('Usage: arena.py <white-server-url> <black-server-url>')
        print('Example: arena.py http://localhost:5001 http://localhost:5002')
        sys.exit(1)

    white_server_url = sys.argv[1]
    black_server_url = sys.argv[2]
    run_arena(white_server_url, black_server_url)


if __name__ == '__main__':
    main()
