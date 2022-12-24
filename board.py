import copy

from PyQt6.QtWidgets import QFrame, QGridLayout
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QPen, QPixmap
# from PyQt6.QtTest import QTest
from piece import Piece


class Board(QFrame):  # base the board on a QFrame widget
    update_timer_signal = pyqtSignal(int)  # signal sent when timer is updated
    click_location_signal = pyqtSignal(str)  # signal sent when there is a new click location
    time_over_signal = pyqtSignal()     # signal sent when timer hit 0

    board_size = 16  # board is 7x7 squares wide

    timer_speed = 1000  # the timer updates every 1 second
    # TODO: counter gonna be 2 mins = 120,000
    counter = 10  # the number the counter will count down from

    background_path = "./icons/board_background.jpg"

    def __init__(self, go):
        super().__init__(go)

        self.go = go

        self.timer = QBasicTimer()  # create a timer for the game
        # TODO: also if timed mode is deactivated count upwards to see how long to make move
        self.is_timed_mode_on = True    # Speed go mode, change this to deactivate game over with timer
        self.is_started = False  # game is not currently started

        # Create a 2d int[7][7] array to store the current state of the game
        self.board_array = [[0 for _ in range(Board.board_size)] for _ in range(Board.board_size)]
        self.pieces_array = []

        self.undo_stack = []
        self.redo_stack = []

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

    def is_move_valid(self, x, y, player):
        """
        Checks if a move is valid in the game of Go.

        This method places a temporary test piece on the board at the given coordinates and checks if it is a valid move
        according to the rules of Go. The move is considered valid if it does not result in self-capture of the group,
        if it captures an enemy group, or if it is adjacent to an empty space.

        :param x: The x coordinate of the move.
        :param y: The y coordinate of the move.
        :param player: The player making the move.
        :return: True if the move is valid, False otherwise.
        """

        test_piece = self.pieces_array[x][y]

        # if the test_piece is already set to a player the move is not valid
        if test_piece.player != 0:
            return False

        # Check if any of the adjacent pieces are empty, if they are the move is immediately valid
        adjacent_piece: Piece
        for adjacent_piece in test_piece.adjacency_list:
            if adjacent_piece.player == 0:
                return True

        # Check if the move will result in self capture of the group, if it does not its valid
        test_piece.player = player  # Easiest way of doing this is by setting the test_piece temporarily

        group_liberty = sum([piece.get_liberties() for piece in test_piece.get_group()])
        if group_liberty > 0:
            return True

        # Check if move is made it will result in capture of enemy group (if it does the move is valid by go rules)
        adjacent_enemy_groups = test_piece.get_adjacent_enemy_groups()

        for enemy_group in adjacent_enemy_groups:
            enemy_group_liberty = sum([piece.get_liberties() for piece in enemy_group])

            if enemy_group_liberty == 0:
                return True

        # If its none of those cases the move is invalid
        test_piece.player = 0  # we reset the piece player to 0 after testing
        return False

    def make_move(self, piece):
        """
        Makes a move on the board by placing the given piece for the current turns player.

        This method first checks if the move is valid. If the move is valid, it places the piece on the board, removes
        any enemy groups that have been captured, and updates the current player. If the move is not valid, it notifies
        the user. TODO: change from printing error message to something in the UI

        :param piece: The piece to be placed on the board.
        """

        # Check if the move is valid
        if not self.is_move_valid(piece.row, piece.column, self.go.current_player):
            print("Invalid Move")
            return

        # Add current state of the board to the undo stack
        self.undo_stack.append((copy.deepcopy(self.board_array), self.go.current_player))

        self.place_piece(piece, self.go.current_player)

        adjacent_enemy_groups = piece.get_adjacent_enemy_groups()

        enemy_group: set[Piece]
        for enemy_group in adjacent_enemy_groups:

            # Gets the enemy test_piece group
            print(enemy_group)

            enemy_group_liberty = sum([piece.get_liberties() for piece in enemy_group])

            if enemy_group_liberty == 0:
                [self.place_piece(piece, 0) for piece in enemy_group]

        # self.print_board_array()
        # print("------------------------------")
        # self.print_piece_array()

        # Empties the redo_stack if there was anything on there
        if self.redo_stack:
            self.redo_stack[:] = []

        self.go.next_turn()

    def print_piece_array(self):

        print("Pieces array:")

        for row in self.pieces_array:
            for piece in row:
                print(piece.player, end="\t")
            print()

    def place_piece(self, piece, player):
        # change reference in board_array
        self.board_array[piece.row][piece.column] = player

        # place the test_piece
        piece.place_piece(player)

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

    def load_state(self, board_state: list[list[int]], player_state: int):
        """
        Loads the given state into the board and updates the current player.

        This method updates the board to reflect the given state. If a piece is already in the correct position, it is
        not modified. Otherwise, the piece is placed as necessary. The current player of the game is also updated based
        on the given player state.

        :param board_state: A 2D list representing the state to be loaded into the board.
        :param player_state: An integer representing whose turn it was at that board state.
        """

        for row, board_row in enumerate(board_state):
            for column, value in enumerate(board_row):

                if self.board_array[row][column] == value:
                    continue

                self.pieces_array[row][column].place_piece(value)

        self.board_array = board_state
        self.go.current_player = player_state

    def undo_move(self):
        """
        Undoes the last move made in the game.

        This method retrieves the last state of the board and current player from the undo stack and loads it into the
        game.
        If the undo stack is empty, this method does nothing. The state that is undone is also added to the redo stack
        for potential future use.
        """

        if not self.undo_stack:
            return

        self.redo_stack.append((copy.deepcopy(self.board_array), self.go.current_player))
        self.load_state(*self.undo_stack.pop())

    def redo_move(self):
        """
        Redoes the previous move that was undone.

        This method retrieves the state of the board and current player from the top of the redo stack and applies it to
        the game.
        The current state of the board and player are then added to the undo stack to allow for future undos.
        """

        if not self.redo_stack:
            return

        self.undo_stack.append((copy.deepcopy(self.board_array), self.go.current_player))
        self.load_state(*self.redo_stack.pop())

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

        # TODO adapt this code to handle your timers to different modes
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if self.is_timed_mode_on and self.counter == 0:
                self.time_over_signal.emit()
                self.timer.stop()
                print("Game over")
                return  # For stop counting down
            self.counter -= 1
            # print('timerEvent()', self.counter)
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
