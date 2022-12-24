from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, QFrame, QHBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSlot, QPoint, Qt


# TODO names, turn counter, timer, skip button

class ScoreBoard(QWidget):
    """ base the score_board on a QLabel"""

    def __init__(self):
        super().__init__()

        self.background = QPixmap("./icons/sb_background.png")
        self.captured_pieces = [0, 0]

        self.players = ["Black", "White"]
        self.current_player = 0
        # TODO: this labels will update with proper signals
        self.player_label = QLabel(self.players[self.current_player])
        self.black_captured = QLabel(str(self.captured_pieces[0]))
        self.white_captured = QLabel(str(self.captured_pieces[1]))
        self.time_label = QLabel("Time Remaining: NA")
        # TODO: this buttons activate signals
        self.undo_btn = QPushButton("Undo")
        self.skip_btn = QPushButton("Skip")
        self.redo_btn = QPushButton("Redo")

        self.init_ui()

    def init_ui(self):
        """initiates ScoreBoard UI"""

        # create a widget to hold other widgets
        main_layout = QVBoxLayout(self)

        # creating line layouts

        # current player layout
        current_player_layout = QVBoxLayout()

        # current player header line
        player_header_line = QHBoxLayout()
        current_player_layout.addLayout(player_header_line)
        # adding stretches to align QLabel
        player_header_line.addStretch()
        player_header_line.addWidget(QLabel("=== Current Player ==="))
        player_header_line.addStretch()

        # label line
        player_label_line = QHBoxLayout()
        current_player_layout.addLayout(player_label_line)
        # adding stretches to align QLabel
        player_label_line.addStretch()
        player_label_line.addWidget(self.player_label)
        player_label_line.addStretch()

        # captured pieces layout
        captured_pieces_layout = QVBoxLayout()

        # captured pieces main header line
        captured_main_header_line = QHBoxLayout()
        captured_pieces_layout.addLayout(captured_main_header_line)
        # adding stretches to align QLabel
        captured_main_header_line.addStretch()
        captured_main_header_line.addWidget(QLabel("=== Captured Pieces ==="))
        captured_main_header_line.addStretch()

        # layout for secondary headers and counters
        pieces_layout = QVBoxLayout()
        captured_pieces_layout.addLayout(pieces_layout)

        # set captured pieces secondary headers line
        pieces_header_line = QHBoxLayout()
        pieces_layout.addLayout(pieces_header_line)
        # adding stretches to align QLabels
        pieces_header_line.addStretch()
        pieces_header_line.addWidget(QLabel("Black"))
        pieces_header_line.addStretch()
        pieces_header_line.addWidget(QLabel("White"))
        pieces_header_line.addStretch()

        # set captured pieces amounts line
        captured_amount_line = QHBoxLayout()
        pieces_layout.addLayout(captured_amount_line)
        # adding stretches to align QLabels
        captured_amount_line.addStretch()
        captured_amount_line.addWidget(self.black_captured)
        captured_amount_line.addStretch()
        captured_amount_line.addWidget(self.white_captured)
        captured_amount_line.addStretch()

        # timer line
        timer_line = QHBoxLayout()
        timer_line.addStretch()
        timer_line.addWidget(self.time_label)
        timer_line.addStretch()

        # buttons line
        buttons_line = QHBoxLayout()
        buttons_line.addStretch()
        buttons_line.addWidget(self.undo_btn)
        buttons_line.addWidget(self.skip_btn)
        buttons_line.addWidget(self.redo_btn)
        buttons_line.addStretch()

        # add all layouts to main layout
        main_layout.addLayout(current_player_layout)
        main_layout.addLayout(captured_pieces_layout)
        main_layout.addLayout(timer_line)
        main_layout.addLayout(buttons_line)


    def make_connection(self, board):
        """this handles a signal sent from the board class"""
        # when the click_location_signal is emitted in board the setClickLocation slot receives it
        board.click_location_signal.connect(self.set_click_location)
        # when the update_timer_signal is emitted in the board the setTimeRemaining slot receives it
        board.update_timer_signal.connect(self.set_time_remaining)
        # when game over due to clock hit zero
        board.time_over_signal.connect(self.game_over)

    @pyqtSlot(str)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def set_click_location(self, click_loc):
        """updates the label to show the click location"""

        print('slot ' + click_loc)

    @pyqtSlot(int)
    def set_time_remaining(self, time_remaining):
        """updates the time remaining label to show the time remaining"""

        update = "Time Remaining: " + str(time_remaining)
        self.time_label.setText(update)
        # print('slot ' + update)
        # self.redraw()

    def change_player(self, player_no):
        self.current_player = player_no
        self.player_label.setText(self.players[self.current_player])

    def game_over(self):
        """updates scoreboard to show scores and winner"""
        self.time_label.setText("Game over, winner " + self.players[self.current_player] + " player")

    # TODO: This could be prettier
    def paintEvent(self, event):
        """paints the board and the pieces of the game"""

        painter = QPainter(self)
        painter.setOpacity(0.5)
        # Draws the board background
        self.background = self.background.scaled(self.width(), self.height())
        painter.drawPixmap(QPoint(), self.background)
