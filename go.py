from itertools import cycle

from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from board import Board
from score_board import ScoreBoard


class Go(QMainWindow):

    def __init__(self):
        super().__init__()

        self.board = Board(self)
        self.score_board = ScoreBoard()
        self.turn_counter = cycle([1, 2])
        self.current_player = next(self.turn_counter)

        self.init_ui()

    def get_board(self):
        return self.board

    def get_score_board(self):
        return self.score_board

    def init_ui(self):
        """initiates application UI"""

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)
        main_layout.addWidget(self.board, 9)
        main_layout.addWidget(self.score_board, 2)

        self.score_board.make_connection(self.board)

        screen = self.screen().availableGeometry()

        self.setMinimumWidth(int(screen.width() * 0.8))
        self.setMinimumHeight(int(screen.height() * 0.88))

        self.setWindowTitle('Go')
        self.show()

    def next_turn(self):
        self.current_player = next(self.turn_counter)
