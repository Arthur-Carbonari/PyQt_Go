from itertools import cycle
from PyQt6.QtGui import QPixmap, QPainter, QIcon, QFont
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, QHBoxLayout, QPushButton, QGroupBox
from PyQt6.QtCore import pyqtSlot, QPoint, QBasicTimer

from Board import Board
from Piece import Piece


# TODO names, turn counter, timer, skip button

class ScoreBoard(QWidget):
    """ base the score_board on a QLabel"""

    timer_speed = 1000  # the timer updates every 1 second
    # TODO: counter gonna be 2 mins = 120,000
    counter = 10  # the number the counter will count down from

    def __init__(self, go, player_names):
        super().__init__()

        self.go = go
        self.background = QPixmap("./icons/sb_background.png")

        self.players = player_names
        self.current_player = 1
        self.player_pool = cycle(self.players)
        self.timers = [QBasicTimer() for _ in self.players]   # create a timer for each player
        self.counters = [ScoreBoard.counter for _ in self.players]
        self.captured_pieces = [0 for _ in self.players]

        self.players_box = None
        self.time_label = QLabel("Time Remaining: NA")

        # TODO: this buttons activate signals
        self.undo_btn = QPushButton("Undo")
        self.skip_btn = QPushButton("Skip")
        self.redo_btn = QPushButton("Redo")

        self.init_ui()

    def init_ui(self):
        """initiates ScoreBoard UI"""

        self.setStyleSheet("QGroupBox{border: 1px solid black;}")

        # create a widget to hold other widgets
        main_layout = QVBoxLayout(self)

        # creating layouts
        # players layout
        self.players_box = self.create_players_boxes()

        # buttons line
        buttons_box = self.create_button_layout()

        # TODO: this is for us to see the timer
        timer_line = QHBoxLayout()
        timer_line.addStretch()
        timer_line.addWidget(self.time_label)
        timer_line.addStretch()

        # add all layouts to main layout
        main_layout.addWidget(self.players_box)
        main_layout.addLayout(timer_line)
        main_layout.addLayout(buttons_box)

    def create_players_boxes(self):
        group_box = QGroupBox()
        group_layout = QVBoxLayout()
        group_box.setLayout(group_layout)
        for i in range(len(self.players)):
            player_no = self.players.index(next(self.player_pool))
            # layout for player card and add it to group_layout
            player_box = QGroupBox()
            player_box_layout = QHBoxLayout()
            player_box.setLayout(player_box_layout)
            group_layout.addWidget(player_box)
            # set icon for player
            player_icon = QLabel()
            player_icon.setPixmap(QIcon(Piece.piece_icons_paths[i+1]).pixmap(64, 64))
            # player information
            player_info_layout = QVBoxLayout()
            # player name
            player_name = QLabel(self.players[player_no])
            player_name.setFont(QFont("serif", 15))
            # TODO: waiting for captured pieces logic
            # captured pieces by player
            captured_pieces = QLabel("Pieces: ",)
            # timer for player
            player_timer = self.counters[player_no]
            player_timer_label = QLabel("Time: " + str(player_timer))

            player_info_layout.addStretch()
            player_info_layout.addWidget(player_name)
            player_info_layout.addWidget(captured_pieces)
            player_info_layout.addWidget(player_timer_label)
            player_info_layout.addStretch()

            player_box_layout.addWidget(player_icon)
            player_box_layout.addLayout(player_info_layout)

        return group_box

    # def create_captured_box(self):
    #     # captured pieces layout
    #     group_box = QGroupBox()
    #     captured_pieces_layout = QVBoxLayout()
    #     group_box.setLayout(captured_pieces_layout)
    #
    #     # captured pieces main header line
    #     captured_main_header_line = QHBoxLayout()
    #     captured_pieces_layout.addLayout(captured_main_header_line)
    #     # adding stretches to align QLabel
    #     captured_main_header_line.addStretch()
    #     captured_main_header_line.addWidget(QLabel("=== Captured Pieces ==="))
    #     captured_main_header_line.addStretch()
    #
    #     # layout for secondary headers and counters
    #     pieces_layout = QVBoxLayout()
    #     captured_pieces_layout.addLayout(pieces_layout)
    #
    #     # set captured pieces secondary headers line
    #     pieces_header_line = QHBoxLayout()
    #     pieces_layout.addLayout(pieces_header_line)
    #     # adding stretches to align QLabels
    #     pieces_header_line.addStretch()
    #     pieces_header_line.addWidget(QLabel("Black"))
    #     pieces_header_line.addStretch()
    #     pieces_header_line.addWidget(QLabel("White"))
    #     pieces_header_line.addStretch()
    #
    #     # set captured pieces amounts line
    #     captured_amount_line = QHBoxLayout()
    #     pieces_layout.addLayout(captured_amount_line)
    #     # adding stretches to align QLabels
    #     captured_amount_line.addStretch()
    #     captured_amount_line.addStretch()
    #
    #     return group_box

    def create_button_layout(self):
        buttons_line = QHBoxLayout()
        buttons_line.addStretch()
        buttons_line.addWidget(self.undo_btn)
        buttons_line.addWidget(self.skip_btn)
        buttons_line.addWidget(self.redo_btn)
        buttons_line.addStretch()
        return buttons_line

    def start(self):
        print("a")
        # TODO: handle this
        # self.timer.start(self.timer_speed, self)  # start the timer with the correct speed

    def make_connection(self, board):
        """this handles a signal sent from the board class"""
        # when the click_location_signal is emitted in board the setClickLocation slot receives it
        board.click_location_signal.connect(self.set_click_location)

    @pyqtSlot(str)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def set_click_location(self, click_loc):
        """updates the label to show the click location"""

        print('slot ' + click_loc)

    @pyqtSlot(int)
    def set_time_remaining(self, time_remaining):
        """updates the time remaining label to show the time remaining"""
        current_player = self.go.current_player

        update = "Time Remaining: " + str(time_remaining)
        # self.time_label.setText(update)
        # print('slot ' + update)
        # self.redraw()

    def change_player(self, player_no):
        self.current_player = player_no
        # TODO: UPDATE WHEEL

    def game_over(self):
        """updates scoreboard to show scores and winner"""
        self.time_label.setText("Game over, " + self.players[(self.current_player + 1) % 2] + " player wins")

    # TODO: This could be prettier
    def paintEvent(self, event):
        """paints the board and the pieces of the game"""

        painter = QPainter(self)
        painter.setOpacity(0.5)
        # Draws the board background
        self.background = self.background.scaled(self.width(), self.height())
        painter.drawPixmap(QPoint(), self.background)

    def timerEvent(self, event):
        """this event is automatically called when the timer is updated. based on the timer_speed variable """
        current_player = self.go.current_player
        # TODO adapt this code to handle your timers to different modes
        # if the timer that has 'ticked' is the one in this class
        if event.timerId() == self.timers[current_player-1].timerId():
            if self.go.is_timed_mode_on and self.counters[current_player] == 0:
                self.go.finish_game()
                self.go.score_board.game_over()
                self.timers[current_player-1].stop()
                print("Game over")
                return  # For stop counting down
            self.counters[current_player] -= 1
            # self.set_time_remaining()
            print('timerEvent()', self.counter)
        else:
            self.go.timerEvent(event)  # if we do not handle an event we should pass it to the super
            # class for handling
