"""
a general player class. If the player type is not specified, this will make random moves.
"""
import random


class Player:

    def __init__(self):
        self.board = None
        self.moves = []
        # if a human player uses the black pieces, the board should be flipped
        self.human = False

    def do_move(self, board):
        self.moves = []
        self.board = board
        for move in self.board.legal_moves:
            self.moves.append(move)
        # select a random move from the legal moves.
        chosen_move = self.moves[random.randrange(0, len(self.moves))]
        return self.board.san(chosen_move)
