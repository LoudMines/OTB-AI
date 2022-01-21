"""
This class is very similar to the speech player class, but slightly more simple because it uses the input function
instead of the microphone input. If anything is unclear, look at speech_player.py as the methods are explained in more
detail there.
"""

from player import Player
from helpers.string_editing import Edit


class ConsolePlayer(Player):

    def __init__(self):
        super().__init__()
        self.human = True
        self.board = None
        self.move = ""
        self.recognized = False
        self.editor = Edit()

    def do_move(self, board):
        self.board = board
        self.recognized = False
        while True:
            try:
                input_text = self.editor.make_chess_notation(input("Input move here: "))
                self.check_for_moves(input_text)
                if self.recognized:
                    return self.move
            except:
                continue

    def check_for_moves(self, text):
        san_list = []
        for move in self.board.legal_moves:
            san_list.append(self.board.san(move))
        san_list.sort(key=len, reverse=True)
        for move in san_list:
            recognizable_move = move.lower()
            recognizable_move = self.editor.remove_check_signs(recognizable_move)
            if text.find(recognizable_move) != -1:
                self.move = move
                self.recognized = True
                print("actual move: " + move)
                break

