"""
This class contains a minimax player with alha-beta pruning. This code is quicker and more compact then
my original version, this version is inspired by the following video by Sebastian Lague:
https://www.youtube.com/watch?v=l-hh51ncgDI&t=587s&ab_channel=SebastianLague
"""

import math

import time

from player import Player
from helpers import constants


class MinimaxPlayer(Player):

    def __init__(self, depth):
        super().__init__()
        self.is_white = False
        self.minimax_called = 0
        self.elapsed_time = 0
        self.depth = depth

    """
    This method runs through all legal moves, and applies minimax to them to determine their heuristic score.
    After each calculation it checks if this leads to a forced checkmate, if so it selects this path without looking 
    at the remaining moves. This is done to increase its speed.
    """
    def do_move(self, board):
        start = time.perf_counter()
        minimax_board = board.copy()
        score_move_pairs = []
        san_move_pairs = []
        sorted_legal_moves = []
        self.minimax_called = 0

        """
        this bit of code makes a list of all legal moves sorted by san length, 
        so checks and captures get looked at first
        """
        for move in minimax_board.legal_moves:
            san_move_pairs.append((minimax_board.san(move), move))
        san_move_pairs.sort(key=len, reverse=True)
        for pair in san_move_pairs:
            # if there is a mate in 1, play this without additional thought
            if pair[0].find("#") != -1:
                finish = time.perf_counter()

                print("found a mate in 1")

                print(f"elapsed time: {finish - start:0.1f} seconds")

                self.elapsed_time += finish - start

                print(f"Total used time: {self.elapsed_time / 60:0.1f}")

                return pair[0]
            sorted_legal_moves.append(pair[1])

        for move in sorted_legal_moves:
            score = self.minimax(minimax_board, move, self.depth, -math.inf, math.inf, False)
            score_move_pairs.append((score, minimax_board.san(move)))
            if score == 100 or score == math.inf:
                break

        print(f"minimax was called: {self.minimax_called} times")

        highest_score, best_move = max(score_move_pairs)

        print(f"best move: {best_move}")
        print(f"with score: {highest_score:0.2f}")

        print(score_move_pairs)

        finish = time.perf_counter()

        if finish - start < 60:
            print(f"elapsed time: {finish - start:0.1f} seconds")
        else:
            print(f"elapsed time: {(finish - start)/60:0.1f} minutes")

        self.elapsed_time += finish - start

        print(f"Total used time: {self.elapsed_time/60:0.1f} \n")

        return best_move

    def minimax(self, current_board, move, depth, alpha, beta, maximizing):
        self.minimax_called += 1

        if depth == 0:
            return self.heuristic_value(current_board)

        current_board.push(move)

        if current_board.is_stalemate() or current_board.is_repetition() or current_board.is_fifty_moves():
            current_board.pop()
            return 0

        if maximizing:
            # start the best score at -infinity and take the max between this and the next score each time
            max_score = -math.inf
            for next_move in current_board.legal_moves:
                # when the desired depth is reached, this will return a heuristic score.
                next_score = self.minimax(current_board, next_move, depth-1, alpha, beta, False)

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

            # remove the pushed move from the board again.
            current_board.pop()

            return max_score
        else:
            min_score = math.inf
            for next_move in current_board.legal_moves:
                next_score = self.minimax(current_board, next_move, depth - 1, alpha, beta, True)

                min_score = min(min_score, next_score)

                beta = min(beta, next_score)

                if alpha >= beta:
                    break

            current_board.pop()

            return min_score

    """
    The heurstic value in chess is a complicated thing. Right now, it tries to get the biggest material advantage
    over its opponent, but this is not optimal in chess. One additional feature is that it ranks knights slightly
    lower when they are on the edge of the board. This is because they have less legal moves here. But to improve the
    AI without increasing the depth, this function should be improved first.
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

        # change the knights' value depending on their location
        for knight_location in current_board.pieces(2, is_white):
            total_value += constants.Constants.knight_values[knight_location]

        total_value += len(current_board.pieces(3, is_white)) * 3  # number of bishops

        total_value += len(current_board.pieces(4, is_white)) * 5  # number of rooks
        total_value += len(current_board.pieces(5, is_white)) * 9  # number of queens
        return total_value
