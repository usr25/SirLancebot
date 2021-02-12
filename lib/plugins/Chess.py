from lib.plugins.Plugin import Plugin

import chess
import chess.pgn


class Chess(Plugin):
    
    board = None

    def __init__(self, data):
        super().__init__("Chess",
                         "Parses a game of blindfold chess. cmd: !chess, !m <move>, !fen, !png",
                         ["chess", "m", "fen", "pgn"])
        self.data = data


    def chess(self, data):
        self.board = chess.Board()
        return "Board initialized"

    def m(self, data):
        err = self.is_board_active()
        if err:
            return err

        move = None

        try:
            if data["args"]:
                move = data["args"][0]
                self.board.push_san(move)
            else:
                return "Supply the move, !m <move>"
        except ValueError as _:
            return f"'{move}' is not a valid move"

        if self.board.is_game_over():
            return "Game over"

    def fen(self, data):
        err = self.is_board_active()
        if err:
            return err

        return self.board.fen()

    def pgn(self, data):
        err = self.is_board_active()
        if err:
            return err

        b_pgn = chess.pgn.Game.from_board(self.board)
        return str(b_pgn.mainline())

    def is_board_active(self):
        if not self.board:
            return "No board has been initialized, try !chess"
        return False