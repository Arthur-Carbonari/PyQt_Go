from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, QFrame
from PyQt6.QtCore import pyqtSlot, QPoint


# TODO names, turn counter, timer, skip button

class ScoreBoard(QWidget):
    """ base the score_board on a QLabel"""
    def __init__(self):
        super().__init__()
        self.background = QPixmap("./icons/sb_background.png")

        self.players = ["Black", "White"]
        # create two labels which will be updated by signals
        self.player_label = QLabel("Current Player: " + self.players[0])
        self.label_click_location = QLabel("Click Location: ")
        self.label_time_remaining = QLabel("Time remaining: ")

        self.init_ui()

    def init_ui(self):
        """initiates ScoreBoard UI"""

        # create a widget to hold other widgets
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.player_label)
        main_layout.addWidget(self.label_click_location)
        main_layout.addWidget(self.label_time_remaining)

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

        self.label_click_location.setText("Click Location:" + click_loc)
        print('slot ' + click_loc)

    @pyqtSlot(int)
    def set_time_remaining(self, time_remaining):
        """updates the time remaining label to show the time remaining"""

        update = "Time Remaining:" + str(time_remaining)
        self.label_time_remaining.setText(update)
        # print('slot ' + update)
        # self.redraw()

    def change_player(self, player_no):
        self.player_label.setText("Current Player: " + self.players[player_no])

    def game_over(self):
        """updates scoreboard to show scores and winner"""
        self.label_time_remaining.setText("Game over, winner" + self.players[next(self.turn_counter)])

    # TODO: This could be prettier
    def paintEvent(self, event):
        """paints the board and the pieces of the game"""

        painter = QPainter(self)
        painter.setOpacity(0.5)
        # Draws the board background
        self.background = self.background.scaled(self.width(), self.height())
        painter.drawPixmap(QPoint(), self.background)
