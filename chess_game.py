import chess

import random

import atexit

import pyttsx3

from helpers.string_editing import Edit


class ChessGame:

    def __init__(self, player1, player2):
        self.narration = False

        self.flipped = False

        # define the players and select a random first player
        self.players = [player1, player2]
        self.current_player = random.randrange(0, 2)

        self.board = chess.Board()
        self.game_finished = False

        self.pgn_text = ""
        self.turn = 0

        self.narrator = pyttsx3.init()

        self.editor = Edit()

        self.players[self.current_player].is_white = True

        # flip the board if the human  player is playing with the black pieces
        if not self.players[self.current_player].human:
            self.flipped = True

    """
    This checks if the board is currently in checkmate and if not, it has the current player make their move.
    If the current player is not a human player, it uses tts to say their move and finally, 
    it adds their move to the game pgn.
    """
    def do_move(self):
        if not self.board.is_game_over():
            move = self.players[self.current_player].do_move(self.board)
            self.board.push_san(move)
            if self.narration and not self.players[self.current_player].human:
                self.say_move(move)

            if self.turn % 2 == 0:
                round_number = int(self.turn/2 + 1)
                self.pgn_text += f"\n {round_number}. {move}"
            else:
                self.pgn_text += f" {move}"

            self.turn += 1
            self.change_player()
        else:
            if not self.game_finished:
                print("game done")
                self.game_finished = True
                print(self.pgn_text)

    def change_player(self):
        # flip the current player index from 1 to 0 or vise versa (this works because the index can only be 1 or 0)
        self.current_player = 1 - self.current_player

    def say_move(self, move):
        # transform the move into something tts can pronounce and say it
        pronounceable = self.editor.make_move_pronounceable(move)
        print(pronounceable)
        self.narrator.say(pronounceable)
        self.narrator.runAndWait()

    def exit_handler(self):
        print(self.pgn_text)

    atexit.register(exit_handler)
