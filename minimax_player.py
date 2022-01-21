"""
This class contains a minimax player with alha-beta pruning. This code is quicker and more compact then
my original version, this version is inspired by the following video by Sebastian Lague:
https://www.youtube.com/watch?v=l-hh51ncgDI&t=587s&ab_channel=SebastianLague
"""

import copy

import math

from player import Player


class MinimaxPlayer(Player):

    def __init__(self):
        super().__init__()
        self.is_white = False
        self.moves = []
        self.minimax_called = 0

    """
    This method runs through all legal moves, and applies minimax to them to determine their heuristic score.
    After each calculation it checks if this leads to a forced checkmate, if so it selects this path without looking 
    at the remaining moves. This is done to increase its speed.
    """
    def do_move(self, board):
        self.board = board
        score_move_pairs = []
        self.minimax_called = 0
        for move in self.board.legal_moves:
            score = self.minimax(self.board, move, 3, -math.inf, math.inf, False)
            score_move_pairs.append((score, self.board.san(move)))
            if score == 100 or score == math.inf:
                break

        print(f"minimax was called: {self.minimax_called} times")

        highest_score, best_move = max(score_move_pairs)

        print(f"best move: {best_move}")
        print(f"with score: {highest_score}")

        return best_move

    def minimax(self, current_board, move, depth, alpha, beta, maximizing):
        self.minimax_called += 1
        if depth == 0:
            return self.heuristic_value(current_board)

        next_board = copy.deepcopy(current_board)
        next_board.push(move)

        if next_board.is_stalemate():
            return 0

        if maximizing:
            # start the best score at -infinity and take the max between this and the next score each time
            max_score = -math.inf
            for next_move in next_board.legal_moves:
                # when the desired depth is reached, this will return a heuristic score.
                next_score = self.minimax(next_board, next_move, depth-1, alpha, beta, False)

                # keeps track of the highest score in the current loop
                max_score = max(max_score, next_score)

                # keeps track of the highest score for the parent node.
                alpha = max(alpha, next_score)

                """
                if the highest score of the parent node becomes greater then the lowest score of the 
                "grand parent", this means the "grand parent" (which is minimizing) had a better 
                option then this node, so this node can be pruned, and we break out of the loop.
                """
                if alpha >= beta:
                    break

            return max_score
        else:
            min_score = math.inf
            for next_move in next_board.legal_moves:
                next_score = self.minimax(next_board, next_move, depth - 1, alpha, beta, True)

                min_score = min(min_score, next_score)

                beta = min(beta, next_score)

                if alpha >= beta:
                    break

            return min_score

    """
    The heurstic value in chess is a complicated thing. Right now, it tries to get the biggest material advantage
    over its opponent, but this is not optimal in chess. Position is also very important. This method of calculating
    the heuristic value also causes it to make semi random moves in the opening. This is the first thing that should 
    be improved to make this ai better.
    """
    def heuristic_value(self, current_board):
        if current_board.is_checkmate():
            if current_board.turn == self.is_white:
                return 100
            else:
                return -100
        own_material = self.calculate_material(current_board, self.is_white)
        opponent_material = self.calculate_material(current_board, not self.is_white)
        score = own_material - opponent_material
        return score

    def calculate_material(self, current_board, is_white):
        # count the number of each piece type this side has and multiply this by its value
        total_value = len(current_board.pieces(1, is_white))  # number of pawns
        total_value += len(current_board.pieces(2, is_white)) * 3  # number of knights
        total_value += len(current_board.pieces(3, is_white)) * 3  # number of bishops
        total_value += len(current_board.pieces(4, is_white)) * 5  # number of rooks
        total_value += len(current_board.pieces(5, is_white)) * 9  # number of queens
        return total_value
