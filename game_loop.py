
from PyQt5.QtCore import QThread, pyqtSignal

from chess_game import ChessGame
from player import Player
from console_player import ConsolePlayer
from speech_player import SpeechPlayer
from minimax_player import MinimaxPlayer

import chess


class GameLoop(QThread):

    send_board = pyqtSignal(chess.Board, bool)

    def __init__(self):
        super().__init__()

        # create the 2 players
        player1 = ConsolePlayer()
        player2 = MinimaxPlayer()

        # create the chess game which keeps track of turns and additional logic
        self.game = ChessGame(player1, player2)

    def run(self):
        while True:
            self.send_board.emit(self.game.board, self.game.flipped)
            self.game.do_move()
            # a small delay to be able to see all the moves
            self.msleep(300)

