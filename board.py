from PyQt6.QtWidgets import QFrame, QGridLayout
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QPen, QPixmap
# from PyQt6.QtTest import QTest
from piece import Piece


class Board(QFrame):  # base the board on a QFrame widget
    update_timer_signal = pyqtSignal(int)  # signal sent when timer is updated
    click_location_signal = pyqtSignal(str)  # signal sent when there is a new click location

    board_size = 16  # board is 7x7 squares wide

    timer_speed = 1000  # the timer updates every 1 second
    counter = 10  # the number the counter will count down from

    background_path = "./icons/board_background.jpg"

    def __init__(self, go):
        super().__init__(go)

        self.go = go

        self.timer = QBasicTimer()  # create a timer for the game
        self.is_started = False  # game is not currently started

        # Create a 2d int[7][7] array to store the current state of the game
        self.board_array = [[0 for _ in range(Board.board_size)] for _ in range(Board.board_size)]
        self.pieces_array = []

        # Create a layout for the board that will contain the Pieces objects
        self.pieces_layout = QGridLayout(self)
        self.pieces_layout.setSpacing(0)

        self.background = QPixmap(Board.background_path)

        # Populate the layout with pieces
        for row in range(Board.board_size):
            piece_row = []
            for column in range(Board.board_size):
                piece = Piece(self, row, column)
                piece_row.append(piece)
                self.pieces_layout.addWidget(piece, row, column)

            self.pieces_array.append(piece_row)

        [[piece.connect_to_adjacent() for piece in piece_row] for piece_row in self.pieces_array]

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

    def try_move(self, x, y):
        """tries to place a piece"""

        # check if move is valid
        if self.game_logic.valid_move(self.go.current_player, x, y):
            self.place_piece(x, y)
            return

        print("invalid")

        # Go to next turn


    def place_piece(self, x, y):
        # change reference in board_array
        self.board_array[x][y] = self.go.current_player

        # place the piece
        current_piece = self.pieces_array[x][y]
        current_piece.place_piece(self.go.current_player)

        # Get the surrounding pieces (up, right, down, left)
        surrounding_pieces = self.game_logic.get_surrounding_pieces(x, y, self.pieces_array)

        # Sets liberty to 0
        current_piece.liberties = 0

        # Updates the liberties for itself and all surrounding pieces
        for surrounding_piece in surrounding_pieces:
            # if the surrounding_piece is an empty piece
            if surrounding_piece.player == 0:
                current_piece.liberties += 1  # increase the new piece liberty by 1
            else:
                surrounding_piece.liberties -= 1  # otherwise decrease the surrounding piece liberty by 1

        for surrounding_piece in surrounding_pieces:
            if current_piece.player == surrounding_piece.player:
                GameLogic.merge_pieces_groups(current_piece, surrounding_piece)

        involved_groups = [current_piece.group]

        for surrounding_piece in surrounding_pieces:
            already_there = False

            if surrounding_piece.player == 0:
                continue

            for group in involved_groups:
                if surrounding_piece.group is group:
                    already_there = True
                    break

            if not already_there:
                involved_groups.append(surrounding_piece.group)

        for group in involved_groups:
            liberty = 0
            for piece in group:
                liberty = liberty + piece.liberties

            if liberty == 0:
                for piece in group:
                    piece.reset_piece()

        self.go.next_turn()

    def print_piece_array(self):

        print("Pieces array:")

        for row in self.pieces_array:
            for piece in row:
                print(piece.player, end="\t")
            print()

    def place_piece(self, piece):
        # change reference in board_array
        self.board_array[piece.row][piece.column] = self.go.current_player

        # place the test_piece
        piece.place_piece(self.go.current_player)

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
