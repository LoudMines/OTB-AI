import speech_recognition

from player import Player
from helpers.string_editing import Edit


class SpeechPlayer(Player):

    def __init__(self):
        super().__init__()
        self.human = True
        self.board = None
        self.move = ""
        self.recognized = False
        self.editor = Edit()

    """
    Listens to the microphone input and tries to turn this in to chess moves. First it uses editor.make_chess_notation
    to convert the input into text the move recognition understands. Then it inserts this string into the 
    check_for_moves method.
    """
    def do_move(self, board):
        self.board = board
        self.recognized = False
        recognizer = speech_recognition.Recognizer()

        while True:
            try:

                with speech_recognition.Microphone() as mic:

                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = recognizer.listen(mic)

                    text = recognizer.recognize_google(audio)

                    input_text = self.editor.make_chess_notation(text)

                    print(f"recognized: {text}")

                    self.check_for_moves(input_text)

                    if self.recognized:
                        return self.move

            except speech_recognition.UnknownValueError:
                recognizer = speech_recognition.Recognizer()
                print("recognized nothing")
                continue
    """
    Creates a list of all legal moves in the notation the user will use (san notation). It then slightly edits these
    and looks for them in the input it received. If the move is in there, it will play it.
    """
    def check_for_moves(self, text):
        san_list = []
        for move in self.board.legal_moves:
            san_list.append(self.board.san(move))
        """
        the list needs to be sorted from longest to shortest to prevent playing the wrong move. For example if the
        player wants to play the move bishop to c4 the san notation is "bc4". However the notation for pawn to 
        c4 is "c4". If the list was not sorted from longest to shortest, it might find "c4" without checking if it 
        is actually supposed to be "bc4". Sorting prevents this. 
        """
        san_list.sort(key=len, reverse=True)
        for move in san_list:
            recognizable_move = move.lower()
            recognizable_move = self.editor.remove_check_signs(recognizable_move)
            if text.find(recognizable_move) != -1:
                self.move = move
                self.recognized = True
                print(f"actual move: {move}")
                break
