from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from board import Board
from score_board import ScoreBoard


class Go(QMainWindow):
    player_changed_signal = pyqtSignal(int)  # signal sent when player changed

    def __init__(self):
        super().__init__()

        self.game_over = False  # TODO: when true seize all operations, merge it with previous one

        self.board = Board(self)
        self.score_board = ScoreBoard()
        self.num_players = 2
        self.current_player = 1

        undo = QShortcut(QKeySequence("Ctrl+Z"), self)
        undo.activated.connect(self.board.undo_move)

        redo = QShortcut(QKeySequence("Ctrl+Y"), self)
        redo.activated.connect(self.board.redo_move)

        self.init_ui()

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
        # make connection with signal with score_board name change
        self.player_changed_signal.connect(self.score_board.change_player)
        self.board.time_over_signal.connect(self.finish_game)

        screen = self.screen().availableGeometry()

        self.setMinimumWidth(int(screen.width() * 0.8))
        self.setMinimumHeight(int(screen.height() * 0.88))

        self.setWindowTitle('Go')
        self.show()

    def next_turn(self):
        self.current_player = (self.current_player % self.num_players) + 1
        self.player_changed_signal.emit(self.current_player-1)
        # TODO: dont reset, change it to the next player, the timer will be accumulative it wont reset on turn pass,
        #  just like in chess

    def finish_game(self):
        self.game_over = True  # GAME OVER
