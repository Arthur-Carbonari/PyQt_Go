# TODO: Add more functions as needed for your Pieces
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QSizePolicy


class Piece(QPushButton):
    NoPiece = 0
    White = 1
    Black = 2
    Status = 0  # default to no piece
    liberties = 0  # default no liberties

    piece_colors = ["#0000",
                    "#fff",
                    "#000"
                    ]

    piece_icons_paths = ["./icons/empty.png",
                         "icons/player_1_piece.png",
                         "icons/player_2_piece.png"
                         ]

    def __init__(self, board, row, column):  # constructor
        super().__init__()
        # self.Status = piece

        self.board = board
        self.row = row
        self.column = column

        self.setStyleSheet(f"border-radius: {self._get_border_radius()}%;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setIcon(QIcon(Piece.piece_icons_paths[0]))

        self.liberties = 0

        self.clicked.connect(self.board.try_move(row, column))

    def place_piece(self):


    def place_piece(self, player):
        self.setIcon(QIcon(Piece.piece_icons_paths[player]))

        self.setStyleSheet(f"""
                    border-radius: {self._get_border_radius()}%;
                    background: {self.piece_colors[player]};
        """)

    def get_piece(self):  # return PieceType
        return self.Status

    def get_liberties(self):  # return Liberties
        return self.liberties

    def set_liberties(self, liberties):  # set Liberties
        self.liberties = liberties

    def _get_border_radius(self):
        """
        This method calculates the maximum valid border radius for the current size of the piece
        :return: maximum border radius value(float)
        """

        return self.height()/2 - 0.6
    # EVENTS =====================================

    def resizeEvent(self, event):
        self.setIconSize(QSize(self.height(), self.width()))

