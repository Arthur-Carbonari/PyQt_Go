from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QSizePolicy


class Piece(QPushButton):
    NoPiece = 0
    White = 1
    Black = 2
    Status = 0  # default to no piece

    piece_colors = ["#0000", "#fff", "#000"]

    piece_icons_paths = ["./icons/empty.png", "icons/player_1_piece.png", "icons/player_2_piece.png"]

    def __init__(self, board, row, column):  # constructor
        super().__init__()
        self.player = 0

        self.board = board
        self.adjacency_list = []
        self.row = row
        self.column = column

        self.setStyleSheet(f"border-radius: {self._get_border_radius()}%;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setIcon(QIcon(Piece.piece_icons_paths[0]))

        self.clicked.connect(self.click_piece)

    def click_piece(self):
        if self.player != 0:
            return

        self.board.try_move(self.row, self.column)

    def place_piece(self, player):
        self.setIcon(QIcon(Piece.piece_icons_paths[player]))

        self.setStyleSheet(f"""
                    border-radius: {self._get_border_radius()}%;
                    background: {self.piece_colors[player]};
        """)

        self.player = player

    def reset_piece(self):
        self.player = 0
        self.setIcon(QIcon(Piece.piece_icons_paths[0]))
        self.setStyleSheet(f"border-radius: {self._get_border_radius()}%;")

    def get_piece(self):  # return PieceType
        return self.Status

    def get_liberties(self):  # return Liberties
        liberty = 0

        for adjacent_piece in self.adjacency_list:
            if adjacent_piece.player == 0:
                liberty += 1

        return liberty

    def connect_to_adjacent(self):
        self.adjacency_list = []

        pieces_array = self.board.pieces_array
        x, y = self.column, self.row

        for (x0, y0) in ((x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)):
            if 0 <= x0 < len(pieces_array) and 0 <= y0 < len(pieces_array):
                self.adjacency_list.append(pieces_array[y0][x0])

    def get_group(self):

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

    def get_adjacent_enemies(self):

        if self.player == 0:
            raise Exception("This test_piece doesnt belong to any player")

        adjacent_enemy_pieces = []

        for adjacent_piece in self.adjacency_list:
            if adjacent_piece.player != 0 and adjacent_piece.player != self.player:
                adjacent_enemy_pieces.append(adjacent_piece)

        return adjacent_enemy_pieces

    def _get_border_radius(self):
        """
        This method calculates the maximum valid border radius for the current size of the piece
        :return: maximum border radius value(float)
        """

        return self.height() / 2 - 0.6

    # EVENTS =====================================

    def resizeEvent(self, event):
        self.setIconSize(QSize(self.height(), self.width()))

        self.setStyleSheet(f"""
                            border-radius: {self._get_border_radius()}%;
                            background: {self.piece_colors[self.player]};
                """)
