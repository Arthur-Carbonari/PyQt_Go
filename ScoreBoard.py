from itertools import cycle
from PyQt6.QtGui import QPixmap, QPainter, QIcon, QFont
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, QHBoxLayout, QPushButton, QGroupBox
from PyQt6.QtCore import pyqtSlot, QPoint, QBasicTimer
from Piece import Piece

class ScoreBoard(QWidget):
    """ base the score_board on a QLabel"""

    timer_speed = 1000  # the timer updates every 1 second
    # TODO: counter going to be 2 mins = 120,000
    counter = 10  # the number the counter will count down from

    def __init__(self, go, player_names):
        super().__init__()

        self.go = go
        self.background = QPixmap("./icons/sb_background.png")

        self.players = player_names
        self.current_player = 0
        self.timer = QBasicTimer()
        self.timer_labels = [QLabel() for _ in self.players]
        self.remaining_time = [ScoreBoard.counter for _ in self.players]
        self.remaining_time[0] += 1   # for delaying timer because when app loading player misses secs

        # TODO: waiting for captured pieces logic
        self.captured_pieces = [0 for _ in self.players]

        self.players_box = None
        self.time_label = QLabel("Time Remaining: NA")

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

        # add all layouts to main layout
        main_layout.addWidget(self.players_box)
        main_layout.addLayout(buttons_box)

    def create_players_boxes(self):
        group_box = QGroupBox()
        group_layout = QVBoxLayout()
        group_box.setLayout(group_layout)
        for player_no in range(len(self.players)):
            # layout for player card and add it to group_layout
            player_box = QGroupBox()
            player_box_layout = QHBoxLayout()
            player_box.setLayout(player_box_layout)
            group_layout.addWidget(player_box)

            # set icon for player
            player_icon = QLabel()
            player_icon.setPixmap(QIcon(Piece.piece_icons_paths[player_no+1]).pixmap(64, 64))

            # player information
            player_info_layout = QVBoxLayout()
            # player name
            player_name = QLabel(self.players[player_no])
            player_name.setFont(QFont("serif", 15))
            # captured pieces by player
            captured_pieces = QLabel("Pieces: " + str(self.captured_pieces[player_no]))
            # timer for player
            player_timer = self.remaining_time[player_no]
            self.timer_labels[player_no].setText("Time: " + str(player_timer))

            player_info_layout.addStretch()
            player_info_layout.addWidget(player_name)
            player_info_layout.addWidget(captured_pieces)
            player_info_layout.addWidget(self.timer_labels[player_no])
            player_info_layout.addStretch()

            player_box_layout.addWidget(player_icon)
            player_box_layout.addLayout(player_info_layout)

        return group_box

    def create_button_layout(self):
        buttons_line = QHBoxLayout()
        buttons_line.addStretch()
        buttons_line.addWidget(self.undo_btn)
        buttons_line.addWidget(self.skip_btn)
        buttons_line.addWidget(self.redo_btn)
        buttons_line.addStretch()
        return buttons_line

    def start(self):
        self.timer.start(self.timer_speed, self) # start the correct timer with the correct speed


    def make_connection(self, board):
        """this handles a signal sent from the board class"""
        # when the click_location_signal is emitted in board the setClickLocation slot receives it
        board.click_location_signal.connect(self.set_click_location)
        # initiate undo move method
        self.undo_btn.clicked.connect(self.go.board.undo_move)
        # initiate skip turn method
        # self.skip_btn.clicked.connect(self.go.board)  #TODO: waiting skip turn logic
        # initiate redo move method
        self.redo_btn.clicked.connect(self.go.board.redo_move)

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
        """changes current player"""
        self.current_player = player_no
        # TODO: UPDATE WHEEL

    def eliminate_player(self):
        """updates scoreboard to show scores and winner"""
        self.timer_labels[self.current_player].setText("Player Eliminated")
        #TODO: elimiate player from using moves


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
        # TODO adapt this code to handle your timers to different modes
        # if the timer that has 'ticked' is the one in this class
        if event.timerId() == self.timer.timerId():
            if self.go.is_timed_mode_on and self.remaining_time[self.current_player] == 0:
                self.go.finish_game()
                self.eliminate_player()
                self.timer.stop()
                print("Game over")
                return  # For stop counting down
            # update counter and timer label on scoreboard
            self.remaining_time[self.current_player] -= 1
            self.timer_labels[self.current_player].setText("Time: " + str(self.remaining_time[self.current_player]))
            # self.set_time_remaining()
            print('timerEvent()', self.remaining_time)
        else:
            self.go.timerEvent(event)  # if we do not handle an event we should pass it to the super
            # class for handling
