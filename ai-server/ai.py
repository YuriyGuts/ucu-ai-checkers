import random


def pick_next_move(board, player):
    # TODO: Implement your AI behavior here.
    # Your code must return an instance of BaseMove (ForwardMove, CaptureMove, or ComboCaptureMove).
    # You can observe how your move impacts the future board state by running `move.apply(board)`.
    # By default, this code will pick a random move from the list of allowed moves.
    return random.choice(board.get_available_moves(player))
