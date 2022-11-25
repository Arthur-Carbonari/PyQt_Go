from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from board import Board
from score_board import ScoreBoard


class Go(QMainWindow):

    def __init__(self):
        super().__init__()

        self.board = Board(self)
        self.score_board = ScoreBoard()

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

        self.resize(800, 800)
        self.center()
        self.setWindowTitle('Go')
        self.show()

    def center(self):
        """centers the window on the screen"""
        gr = self.frameGeometry()
        screen = self.screen().availableGeometry().center()

        gr.moveCenter(screen)
        self.move(gr.topLeft())
        # size = self.geometry()
        # self.move((screen.width() - size.width()) / 2,(screen.height() - size.height()) / 2)
