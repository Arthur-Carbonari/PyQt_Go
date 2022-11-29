from PyQt6.QtWidgets import QFrame, QGridLayout
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QPoint
from PyQt6.QtGui import QPainter, QPen, QPixmap
# from PyQt6.QtTest import QTest
from piece import Piece


class Board(QFrame):  # base the board on a QFrame widget
    update_timer_signal = pyqtSignal(int)  # signal sent when timer is updated
    click_location_signal = pyqtSignal(str)  # signal sent when there is a new click location

    board_size = 7  # board is 7x7 squares wide

    timer_speed = 1000  # the timer updates every 1 second
    counter = 10  # the number the counter will count down from

    background_path = "./icons/board_background.jpg"

    def __init__(self, parent):
        super().__init__(parent)

        self.timer = QBasicTimer()  # create a timer for the game
        self.is_started = False  # game is not currently started

        # Create a 2d int[7][7] array to store the current state of the game
        self.board_array = [[0] * Board.board_size] * Board.board_size

        # Create a layout for the board that will contain the Pieces objects
        self.pieces_layout = QGridLayout(self)
        self.pieces_layout.setSpacing(0)

        self.background = QPixmap(Board.background_path)

        # Populate the layout with pieces
        for row in range(Board.board_size):
            for column in range(Board.board_size):
                piece = Piece(row, column)
                self.pieces_layout.addWidget(piece, row, column)

        self.init_board()

    def init_board(self):
        """initiates board"""

        self.start()  # start the game which will start the timer

        self.print_board_array()

    def print_board_array(self):
        """prints the board_array to the terminal in an attractive way"""

        print("board_array:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.board_array]))

    def mouse_pos_to_col_row(self, event):
        """convert the mouse click event to a row and column"""

    def square_size(self):
        """returns the side size of one square in the board"""

        return int(self.contentsRect().width() / (Board.board_size + 1))

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

        # set the default colour of the brush
        painter.setPen(QPen(Qt.GlobalColor.black, 3))

        square_width = self.square_size()

        board_start = square_width
        board_end = square_width * Board.board_size
        xy_position: int

        for i in range(1, Board.board_size + 1):

            xy_position = square_width * i

            # draws the rows
            painter.drawLine(board_start, xy_position, board_end, xy_position)

            # Draws the columns
            painter.drawLine(xy_position, board_start, xy_position, board_end)

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
                radius = self.square_size() / 4
                center = QPointF(radius, radius)
                painter.drawEllipse(center, radius, radius)
                painter.restore()

    # EVENTS ===========================================

    def resizeEvent(self, event):

        # This makes so that the board is always square, since most monitors are larger horizontally, it limits the
        # board size by height.
        self.setFixedWidth(self.height())

        # Update the margin of the layout so that the pieces are always at the intersection of the board squares
        space = int(self.square_size() * 0.5)
        end_space = int(self.width() - space - Board.board_size * self.square_size())

        self.pieces_layout.setContentsMargins(space, space, end_space, end_space)

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

        painter = QPainter(self)

        # Draws the board background
        self.background = self.background.scaled(self.width(), self.height())
        painter.drawPixmap(QPoint(), self.background)

        # Draws the board squares
        self.draw_board_squares(painter)

    def mousePressEvent(self, event):
        """this event is automatically called when the mouse is pressed"""

        click_loc = "click location [" + str(event.position().x()) + "," + str(
            event.position().y()) + "]"  # the location where a mouse click was registered
        print("mousePressEvent() - " + click_loc)
        # TODO you could call some game logic here
        self.click_location_signal.emit(click_loc)
