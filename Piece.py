from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QPushButton, QSizePolicy, QGraphicsDropShadowEffect

from Settings import Settings


class Piece(QPushButton):
    # NoPiece = 0
    # Black = 1
    # White = 2

    def __init__(self, board, row: int, column: int):  # constructor
        """
        Initializes a Piece object.

        :param board: The board object that this Piece object is a part of.
        :param row: The row position of this Piece object in the board.
        :param column: The column position of this Piece object in the board.
        """

        super().__init__()
        self.player = 0

        self.board = board
        self.adjacency_list = []
        self.row = row
        self.column = column

        self.setObjectName("free")

        self.setStyleSheet(f"""
        border-radius: {self._get_border_radius()}%;
        """)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setIcon(QIcon(Settings.PIECE_ICONS_PATHS[0]))

        self.clicked.connect(self.click_piece)

    def click_piece(self):
        """
        Handles a click event on this piece.

        If this piece is already occupied by a player, nothing happens. Otherwise, the make_move method of the
        associated Go Game is called with this piece as an argument.
        """

        if self.player != 0:
            return

        self.board.go.make_move(self)

    def place_piece(self, player: int):
        """
       Places a piece on this Piece object.

       :param player: The player to place on this Piece object.
       """

        self.player = player
        self.setIcon(QIcon(Settings.PIECE_ICONS_PATHS[self.player]))
        self.setStyleSheet(f"""
                    border-radius: {self._get_border_radius()}%;
                    background: {Settings.PIECE_COLORS[self.player]};
        """)

        if player == 0:
            self.setObjectName("free")
        else:
            self.setObjectName("")

    def get_liberties(self) -> int:
        """
        Returns the number of liberties that this Piece object has.

        :return: The number of liberties that this Piece object has.
        """

        liberty = 0

        for adjacent_piece in self.adjacency_list:
            if adjacent_piece.player == 0:
                liberty += 1

        return liberty

    def connect_to_adjacent(self):
        """
        Connects this Piece object to its adjacent Piece objects.
        """

        self.adjacency_list = []

        pieces_array = self.board.pieces_array
        x, y = self.column, self.row

        for (x0, y0) in ((x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)):
            if 0 <= x0 < len(pieces_array) and 0 <= y0 < len(pieces_array):
                self.adjacency_list.append(pieces_array[y0][x0])

    def get_group(self):
        """
        Returns the group of Piece objects that this Piece object belongs to.

        :return: The group of Piece objects that this Piece object belongs to.
        :rtype: set[Piece]
        """

        if self.player == 0:
            raise Exception("This test_piece doesnt belong to any player")

        group: set[Piece] = set()

        to_check = [self]
        checked = set()

        while to_check:
            piece = to_check.pop()
            group.add(piece)

            adjacent_piece: Piece
            for adjacent_piece in piece.adjacency_list:
                if adjacent_piece.player == self.player and adjacent_piece not in checked:
                    to_check.append(adjacent_piece)

            checked.add(piece)

        return group

    def get_adjacent_enemies_pieces(self):
        """
        Returns a list of the adjacent Piece objects that belong to an opposing player.

        :return: A list of the adjacent Piece objects that belong to an opposing player.
        :rtype: list[Piece]
        """

        if self.player == 0:
            raise Exception("This test_piece doesnt belong to any player")

        adjacent_enemy_pieces = []

        for adjacent_piece in self.adjacency_list:
            if adjacent_piece.player != 0 and adjacent_piece.player != self.player:
                adjacent_enemy_pieces.append(adjacent_piece)

        return adjacent_enemy_pieces

    def get_adjacent_enemy_groups(self):
        """
        Returns a list of the groups of Piece objects that the adjacent enemies Piece objects belong to.

        :return: A list of the group of Piece objects that the adjacent enemies Piece objects belong to.
        :rtype: list[set[Piece]]
        """

        adjacent_enemy_groups = []

        adjacent_enemy: Piece
        for adjacent_enemy in self.get_adjacent_enemies_pieces():

            # Checks if the adjacent enemy is in any of the previous identified enemy groups
            if any([adjacent_enemy in enemy_group for enemy_group in adjacent_enemy_groups]):
                continue

            adjacent_enemy_groups.append(adjacent_enemy.get_group())

        return adjacent_enemy_groups

    def _get_border_radius(self) -> float:
        """
        Calculates the maximum valid border radius for the current size of this Piece object.

        :return: The maximum border radius value (float).
        :rtype: float
        """

        return self.height() / 2 - 0.6

    # EVENTS =====================================

    def resizeEvent(self, event):
        """
        Handles the resize event for this Piece object.

        :param event: The resize event object.
        :type event: QResizeEvent
        """

        self.setIconSize(QSize(self.height(), self.width()))

        self.setStyleSheet(f"""
                            QPushButton{{
                                background: {Settings.PIECE_COLORS[self.player]};
                                border-radius: {self._get_border_radius()}%;
                            
                            }}          
                """)

    # TO STRING METHODS ===========================

    def __str__(self):
        return f"(Player: '{self.player}', X: '{self.column}', Y: '{self.row}')"

    def __repr__(self):
        return f"(Player: '{self.player}', X: '{self.column}', Y: '{self.row}')"
