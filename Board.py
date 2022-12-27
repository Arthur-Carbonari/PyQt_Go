import copy

from PyQt6.QtWidgets import QFrame, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QPen, QPixmap
# from PyQt6.QtTest import QTest
from Piece import Piece
from Settings import Settings


class Board(QFrame):  # base the board on a QFrame widget
    click_location_signal = pyqtSignal(str)  # signal sent when there is a new click location

    background_path = "./icons/board_background.jpg"

    def __init__(self, go, board_size=16):
        super().__init__(go)

        self.go = go
        self.board_size = board_size

        self.is_started = False  # game is not currently started

        # Create a 2d int[7][7] array to store the current state of the game
        self.board_array = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.pieces_array = []

        # Create a layout for the board that will contain the Pieces objects
        self.pieces_layout = QGridLayout(self)
        self.pieces_layout.setSpacing(0)

        self.background = QPixmap(Board.background_path)

        # Populate the layout with pieces
        for row in range(self.board_size):
            piece_row = []
            for column in range(self.board_size):
                piece = Piece(self, row, column)
                piece_row.append(piece)
                self.pieces_layout.addWidget(piece, row, column)

            self.pieces_array.append(piece_row)

        [[piece.connect_to_adjacent() for piece in piece_row] for piece_row in self.pieces_array]

        self.init_board()

    def init_board(self):
        """initiates board"""
        self.print_board_array()

    def print_board_array(self):
        """prints the board_array to the terminal in an attractive way"""

        print("board_array:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.board_array]))

    def mouse_pos_to_col_row(self, event):
        """convert the mouse click event to a row and column"""

    def square_size(self):
        """returns the side size of one square in the board"""

        return int(self.contentsRect().width() / (self.board_size + 1))

    def reset(self):
        """clears pieces from the board"""

        [[self.place_piece(piece, 0) for piece in piece_row] for piece_row in self.pieces_array]

    def get_current_state(self):
        return copy.deepcopy(self.board_array)

    def set_player_turn(self, player_number):
        self.setStyleSheet(f"""
                QPushButton#free:hover{{
                                        border: 2px solid {Settings.PIECE_COLORS[player_number]}; 
                                    }}     
                """)

    def is_move_valid(self, row, column, player):
        """
        Checks if a move is valid in the game of Go.

        This method places a temporary test piece on the board at the given coordinates and checks if it is a valid move
        according to the rules of Go. The move is considered valid if it does not result in self-capture of the group,
        if it captures an enemy group, or if it is adjacent to an empty space.

        :param row: The x coordinate of the move.
        :param column: The y coordinate of the move.
        :param player: The player making the move.
        :return: True if the move is valid, False otherwise.
        """

        test_piece = self.pieces_array[row][column]

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

    def capture_surrounding_pieces(self, piece) -> int:
        pieces_captured = 0

        adjacent_enemy_groups = piece.get_adjacent_enemy_groups()

        enemy_group: set[Piece]
        for enemy_group in adjacent_enemy_groups:
            enemy_group_liberty = sum([piece.get_liberties() for piece in enemy_group])

            if enemy_group_liberty == 0:
                pieces_captured += len(enemy_group)
                [self.place_piece(piece, 0) for piece in enemy_group]

        return pieces_captured

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
        board_end = square_width * self.board_size
        xy_position: int

        for i in range(1, self.board_size + 1):
            xy_position = square_width * i

            # draws the rows
            painter.drawLine(board_start, xy_position, board_end, xy_position)

            # Draws the columns
            painter.drawLine(xy_position, board_start, xy_position, board_end)

    def load_state(self, board_state: list[list[int]]):
        """
        Loads the given state into the board.

        This method updates the board to reflect the given state. If a piece is already in the correct position, it is
        not modified. Otherwise, the piece is placed as necessary. The current player of the game is also updated based
        on the given player state.

        :param board_state: A 2D list representing the state to be loaded into the board.
        """

        for row, board_row in enumerate(board_state):
            for column, value in enumerate(board_row):

                if self.board_array[row][column] == value:
                    continue

                self.pieces_array[row][column].place_piece(value)

        self.board_array = board_state

    def get_controlled_territories(self):
        """Find the owners and the territories of the whole board"""

        territories = {player_no + 1: set()
                       for player_no in range(self.go.num_players)}

        # for each space in board
        for x in range(self.board_size):
            for y in range(self.board_size):
                # if area is empty return area with player that controls it
                if self.board_array[x][y] == 0 and (x, y) not in set().union(*territories.values()):
                    owner, terr = self.territory(x, y)
                    if owner and terr:
                        territories[owner] = territories[owner].union(terr)

        return territories

    def territory(self, x, y):
        """Find the owner of given space in board"""

        def valid_space(x2, y2):
            return 0 <= x2 < self.board_size and 0 <= y2 < self.board_size

        def grow_territory(x1, y1):
            """if space is not already in set: add space to set and control adjacent spaces"""
            nonlocal territory
            # if territory already has the space return
            if (x1, y1) in territory:
                return
            # add space to set
            territory.add((x1, y1))
            # for every adjacent space
            for n in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                x2 = x1 + n[0]
                y2 = y1 + n[1]
                # control if space is valid and empty
                if valid_space(x2, y2) and self.board_array[x2][y2] == 0:
                    grow_territory(x2, y2)

        # if space isn't empty return
        if self.board_array[x][y] != 0:
            return 0, set()

        # check the y-axis upwards
        for y1 in range(y - 1, -1, -1):
            # if space is not empty break
            if self.board_array[x][y1] != 0:
                owner = self.board_array[x][y1]
                break
        # if loop did not encounter a break
        else:
            # check y-axis downwards
            for y1 in range(y + 1, self.board_size):
                if self.board_array[x][y1] != 0:
                    owner = self.board_array[x][y1]
                    break
            # if loop did not encounter a break
            else:
                # check x-axis to right side
                for x1 in range(x + 1, self.board_size):
                    owner = self.board_array[x1][y]
                    break
                    # if loop did not encounter a break
                else:
                    for x1 in range(x - 1, -1, -1):
                        owner = self.board_array[x1][y]
                        break
                        # if loop did not encounter a break
                    else:
                        owner = 0

        territory = set()
        grow_territory(x, y)
        try:
            for space in territory:
                # for every adjacent space in territory
                for n in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    xt = space[0] + n[0]
                    yt = space[1] + n[1]
                    # if adjacent space has enemy piece
                    if valid_space(xt, yt) and self.board_array[xt][yt] not in [owner, 0]:  # Bounded by enemy
                        owner = 0
                        raise StopIteration
        except StopIteration:
            pass

        return owner, territory

    # EVENTS ===========================================

    def resizeEvent(self, event):

        # This makes so that the board is always square, since most monitors are larger horizontally, it limits the
        # board size by height.
        self.setFixedWidth(self.height())

        # Update the margin of the layout so that the pieces are always at the intersection of the board squares
        space = int(self.square_size() * 0.5)
        end_space = int(self.width() - space - self.board_size * self.square_size())

        self.pieces_layout.setContentsMargins(space, space, end_space, end_space)

    def paintEvent(self, event):
        """paints the board and the pieces of the game"""

        painter = QPainter(self)

        # Draws the board background
        self.background = self.background.scaled(self.width(), self.height())
        painter.drawPixmap(QPoint(), self.background)

        # Draws the board squares
        self.draw_board_squares(painter)
