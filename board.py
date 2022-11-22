from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF
from PyQt6.QtGui import QPainter
# from PyQt6.QtTest import QTest
# from piece import Piece


class Board(QFrame):  # base the board on a QFrame widget
    update_timer_signal = pyqtSignal(int)  # signal sent when timer is updated
    click_location_signal = pyqtSignal(str)  # signal sent when there is a new click location

    board_width = 7  # board is 7 squares wide
    board_height = 7  #
    timer_speed = 1000  # the timer updates every 1 second
    counter = 10  # the number the counter will count down from

    def __init__(self, parent):
        super().__init__(parent)

        self.timer = QBasicTimer()  # create a timer for the game
        self.is_started = False  # game is not currently started
        self.board_array = []  # TODO - create a 2d int/Piece array to store the state of the game

        self.init_board()

    def init_board(self):
        """initiates board"""

        self.start()  # start the game which will start the timer

        # self.printBoardArray()    # TODO - uncomment this method after creating the array above

    def print_board_array(self):
        """prints the board_array in an attractive way"""

        print("board_array:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.board_array]))

    def mouse_pos_to_col_row(self, event):
        """convert the mouse click event to a row and column"""

    def square_width(self):
        """returns the width of one square in the board"""

        return self.contentsRect().width() / self.board_width

    def square_height(self):
        """returns the height of one square of the board"""

        return self.contentsRect().height() / self.board_height

    def start(self):
        """starts game"""

        self.is_started = True  # set the boolean which determines if the game has started to TRUE
        self.reset_game()  # reset the game
        self.timer.start(self.timer_speed, self)  # start the timer with the correct speed

        print("start () - timer is started")

    def reset_game(self):
        """clears pieces from the board"""

        # TODO write code to reset game

    def try_move(self, new_x, new_y):
        """tries to move a piece"""

    def draw_board_squares(self, painter: QPainter):
        """draw all the square on the board"""

        # TODO set the default colour of the brush
        for row in range(0, Board.board_height):
            for col in range(0, Board.board_width):
                painter.save()

                # TODO set this value equal the transformation in the column direction
                col_transformation = self.square_width() * col

                # TODO set this value equal the transformation in the row direction
                row_transformation = 0

                painter.translate(col_transformation, row_transformation)
                painter.fillRect()  # TODO provide the required arguments
                painter.restore()
                # TODO change the colour of the brush so that a checkered board is drawn

    def draw_pieces(self, painter: QPainter):
        """draw the prices on the board"""

        colour = Qt.GlobalColor.transparent  # empty square could be modeled with transparent pieces
        painter.setPen(colour)

        for row in range(0, len(self.board_array)):
            for col in range(0, len(self.board_array[0])):
                painter.save()
                painter.translate()

                # TODO draw some the pieces as ellipses
                # TODO choose your colour and set the painter brush to the correct colour
                radius = self.square_width() / 4
                center = QPointF(radius, radius)
                painter.drawEllipse(center, radius, radius)
                painter.restore()

    # EVENTS ===========================================

    def timerEvent(self, event):
        """this event is automatically called when the timer is updated. based on the timer_speed variable """

        # TODO adapt this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if Board.counter == 0:
                print("Game over")
            self.counter -= 1
            print('timerEvent()', self.counter)
            self.update_timer_signal.emit(self.counter)
        else:
            super(Board, self).timerEvent(event)  # if we do not handle an event we should pass it to the super
            # class for handling

    def paintEvent(self, event):
        """paints the board and the pieces of the game"""

        # painter = QPainter(self)
        # self.drawBoardSquares(painter)
        # self.drawPieces(painter)

    def mousePressEvent(self, event):
        """this event is automatically called when the mouse is pressed"""

        click_loc = "click location [" + str(event.position().x()) + "," + str(
            event.position().y()) + "]"  # the location where a mouse click was registered
        print("mousePressEvent() - " + click_loc)
        # TODO you could call some game logic here
        self.click_location_signal.emit(click_loc)
