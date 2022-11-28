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
    row = -1
    column = -1

    def __init__(self, row, column):  # constructor
        super().__init__()
        # self.Status = piece

    def __init__(self, piece, x, y):  # constructor
        self.Status = piece
        self.liberties = 0
        self.row = row
        self.column = column


    def get_piece(self):  # return PieceType
        return self.Status

    def get_liberties(self):  # return Liberties
        return self.liberties

    def set_liberties(self, liberties):  # set Liberties
        self.liberties = liberties
