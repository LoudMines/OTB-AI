"""
There is a lot of static string editing that needs to happen for speech recognition and tts. To not clog up other
classes, all the string editing ha been moved to this class.
"""


class Edit:
    @staticmethod
    def make_move_pronounceable(move):
        move = move.lower()
        check_status = ""
        # calculate the length of the string removing any check marks
        if "+" in move:
            check_status = " check"
            move = move[0:len(move) - 1]
        elif "#" in move:
            check_status = " checkmate"
            move = move[0:len(move) - 1]

        # castling
        if move == "o-o":
            pronounceable_move = "castles"
        elif move == "o-o-o":
            pronounceable_move = "long castle"

        # separating rank from file for pronunciation
        elif len(move) == 2:
            pronounceable_move = move[0:1] + ' ' + move[1:]

        # pronouncing the piece names if they are just moving
        elif len(move) == 3:
            if move[0] == "r":
                pronounceable_move = move.replace("r", "rook ")
            elif move[0] == "k":
                pronounceable_move = move.replace("k", "king ")
            elif move[0] == "n":
                pronounceable_move = move.replace("n", "knight ")
            elif move[0] == "b":
                pronounceable_move = move.replace("b", "bishop ")
            elif move[0] == "q":
                pronounceable_move = move.replace("q", "queen ")

        elif len(move) == 4:
            if "x" in move:
                pronounceable_move = move.replace("x", " takes ")
                if move[0] == "r":
                    pronounceable_move = pronounceable_move.replace("r", "rook ")
                elif move[0] == "k":
                    pronounceable_move = pronounceable_move.replace("k", "king ")
                elif move[0] == "n":
                    pronounceable_move = pronounceable_move.replace("n", "knight ")
                elif move[0] == "q":
                    pronounceable_move = pronounceable_move.replace("q", "queen ")
            elif "=" in move:
                pronounceable_move = move
            else:
                if move[0] == "r":
                    pronounceable_move = move.replace("r", "rook ")
                elif move[0] == "n":
                    pronounceable_move = move.replace("n", "knight ")
                elif move[0] == "b":
                    pronounceable_move = move.replace("b", "bishop ")
                elif move[0] == "q":
                    pronounceable_move = move.replace("q", "queen ")

        elif len(move) == 5:
            if move[0] == "r":
                pronounceable_move = move.replace("r", "rook ")
            elif move[0] == "k":
                pronounceable_move = move.replace("k", "king ")
            elif move[0] == "n":
                pronounceable_move = move.replace("n", "knight ")
            elif move[0] == "b":
                pronounceable_move = move.replace("b", "bishop ")
            elif move[0] == "q":
                pronounceable_move = move.replace("q", "queen ")

        elif len(move) == 6:
            if "x" in move:
                pronounceable_move = move.replace("x", " takes ")

        return pronounceable_move + check_status

    @staticmethod
    def make_chess_notation(string):
        string = string.replace(" ", "")
        string = string.lower()
        # words to digits
        string = string.replace("one", "1")
        string = string.replace("two", "2")
        string = string.replace("three", "3")
        string = string.replace("four", "4")
        string = string.replace("five", "5")
        string = string.replace("six", "6")
        string = string.replace("seven", "7")
        string = string.replace("eight", "8")
        # pieces to letters
        string = string.replace("rook", "r")
        string = string.replace("knight", "n")
        string = string.replace("night", "n")
        string = string.replace("bishop", "b")
        string = string.replace("queen", "q")
        string = string.replace("king", "k")
        # miscellaneous
        string = string.replace("takes", "x")
        string = string.replace("equals", "=")
        string = string.replace("is", "=")
        return string

    @staticmethod
    def remove_check_signs(string):
        string = string.replace("+", "")
        string = string.replace("#", "")
        return string
