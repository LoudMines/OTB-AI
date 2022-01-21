"""
Final Project by Luit Meinen, last edited on the 20th of January.
Required libraries: Chess, pyqt5, speech_recognition and pyttsx3
Main class: runs the QSVGWidget and starts the game loop thread
"""
import chess
import chess.svg

import sys

from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication

from game_loop import GameLoop


class MainWindow(QSvgWidget):

    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 1000, 1000)

        # create the window
        self.window = QSvgWidget(parent=self)
        self.window.setGeometry(10, 10, 950, 950)

        # initialize the board svg
        self.chessboardSvg = ""

        # create and start the game_loop.py thread
        self.gameLoop = GameLoop()
        self.gameLoop.start()
        self.gameLoop.send_board.connect(self.load_board)

    def load_board(self, board, flipped):
        self.chessboardSvg = chess.svg.board(board, flipped=flipped).encode("UTF-8")
        self.window.load(self.chessboardSvg)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())