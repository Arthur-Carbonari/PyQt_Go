from PyQt6.QtGui import QPixmap, QPainter, QIcon, QFont
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, QHBoxLayout, QPushButton, QGroupBox
from PyQt6.QtCore import QPoint
from Piece import Piece
from Settings import Settings


class ScoreBoard(QWidget):
    """ base the score_board on a QLabel"""

    def __init__(self, go, players_names):
        super().__init__(go)

        self.background = QPixmap("./icons/sb_background.png")

        self.number_of_players = len(players_names)

        self.players_boxes = [PlayerBox(self, i, name) for i, name in enumerate(players_names)]
        self.players_boxes_layout = QVBoxLayout()
        [self.players_boxes_layout.addWidget(widget) for widget in self.players_boxes]

        self.undo_btn = QPushButton("Undo")
        self.undo_btn.clicked.connect(go.undo_move)

        self.skip_btn = QPushButton("Skip")
        self.skip_btn.clicked.connect(go.pass_turn)

        self.redo_btn = QPushButton("Redo")
        self.redo_btn.clicked.connect(go.redo_move)

        self.init_ui()

    def init_ui(self):
        """initiates ScoreBoard UI"""

        self.setStyleSheet(Settings.SCORE_BOARD_STYLESHEET)

        main_group_box = QGroupBox(self)
        main_layout = QVBoxLayout(main_group_box)

        # creating layouts
        # players layout
        players_box = self.create_players_boxes()

        # buttons line
        buttons_box = self.create_button_layout()

        # add all layouts to main layout
        main_layout.addStretch(2)
        main_layout.addWidget(players_box, 14)
        main_layout.addStretch(1)
        main_layout.addLayout(buttons_box, 1)
        main_layout.addStretch(1)

        main_wrapper_layout = QVBoxLayout(self)
        main_wrapper_layout.addWidget(main_group_box)
        main_wrapper_layout.setContentsMargins(0, 0, 0, 0)

    def create_players_boxes(self):
        group_box = QGroupBox(self)

        inner_wrapper_layout = QVBoxLayout()
        inner_wrapper_layout.addStretch(1)
        inner_wrapper_layout.addLayout(self.players_boxes_layout)
        inner_wrapper_layout.addStretch(3)

        group_box.setLayout(inner_wrapper_layout)

        return group_box

    def create_button_layout(self):
        buttons_line = QHBoxLayout()
        buttons_line.addStretch()
        buttons_line.addWidget(self.undo_btn)
        buttons_line.addWidget(self.skip_btn)
        buttons_line.addWidget(self.redo_btn)
        buttons_line.addStretch()
        return buttons_line

    def reset(self):
        [player_box.reset() for player_box in self.players_boxes]
        self.set_turn_player(1)

    def next_turn(self):
        last_turns_player = self.players_boxes_layout.itemAt(0).widget()
        last_turns_player.setStyleSheet('')
        self.players_boxes_layout.removeWidget(last_turns_player)
        self.players_boxes_layout.addWidget(last_turns_player)

        self.players_boxes_layout.itemAt(0).widget().setStyleSheet(Settings.CURRENT_PLAYER_STYLESHEET)

    def set_turn_player(self, player_number: int):
        """changes current player"""
        player_index = player_number - 1
        self.players_boxes_layout.itemAt(0).widget().setStyleSheet("")

        [self.players_boxes_layout.removeWidget(player_box) for player_box in self.players_boxes_layout.children()]

        new_player_order = self.players_boxes[player_index:] + self.players_boxes[:player_index]
        [self.players_boxes_layout.addWidget(player_box) for player_box in new_player_order]

        new_player_order[0].setStyleSheet(Settings.CURRENT_PLAYER_STYLESHEET)

        # effect = QGraphicsDropShadowEffect()
        # effect.setColor(QColor(255, 255, 0))  # Set the color to yellow
        # effect.setBlurRadius(10)  # Set the intensity of the glow
        # first_widget.setGraphicsEffect(effect)

    def highlight_winner(self, winner_player: int):

        self.set_turn_player(winner_player)

        for player_box in self.players_boxes:
            player_box.setObjectName("loser")

        self.players_boxes[winner_player - 1].setObjectName("winner")

        for player_box in self.players_boxes:
            player_box.setStyleSheet("""
                PlayerBox#loser{
                    border: 2px solid #8B0000;
                    border-radius: 5px;
                    box-shadow: 0 0 10px #8B0000;
                }
                PlayerBox#winner{
                    border: 2px solid #0000FF;
                    border-radius: 5px;
                    box-shadow: 0 0 10px #0000FF;
                }
        """)

    # EVENTS ===========================================
    def paintEvent(self, event):
        """paints the board and the pieces of the game"""

        painter = QPainter(self)
        # painter.setOpacity(0.5)
        # Draws the board background
        self.background = self.background.scaled(self.width(), self.height())
        painter.drawPixmap(QPoint(), self.background)

    def update_player_capture(self, player_id: int, captured_pieces_total: int):
        self.players_boxes[player_id - 1].set_captured_pieces_label(captured_pieces_total)

    def update_player_time(self, player_id: int, remaining_time: int):
        self.players_boxes[player_id - 1].set_timer_label(remaining_time)

    # EVENTS ====================================================

    def resizeEvent(self, event) -> None:
        self.setMaximumWidth(int(self.parent().width() * 0.35))


class PlayerBox(QGroupBox):

    def __init__(self, score_board, player_number, player_name="Default Name"):
        super().__init__(score_board)

        self.score_board = score_board

        self.player_name_label = QLabel(player_name)
        self.player_name_label.setFont(QFont("serif", 15))

        self.captured_pieces_label = QLabel("Captured Pieces: 0")
        self.timer_label = QLabel("Time: --")
        self.player_icon = QLabel()
        self.player_icon.setPixmap(QIcon(Settings.PIECE_ICONS_PATHS[player_number + 1]).pixmap(64, 64))
        
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        main_layout.addWidget(self.player_icon)

        info_layout = QVBoxLayout()

        info_layout.addStretch()
        info_layout.addWidget(self.player_name_label)
        info_layout.addWidget(self.captured_pieces_label)
        info_layout.addWidget(self.timer_label)
        info_layout.addStretch()

        main_layout.addLayout(info_layout)

    def set_captured_pieces_label(self, captured_pieces: int):
        self.captured_pieces_label.setText("Captured Pieces: " + str(captured_pieces))

    def set_timer_label(self, time: int):
        self.timer_label.setText("Time: " + str(time))

    def reset(self):
        self.captured_pieces_label = QLabel("Captured Pieces: 0")
        self.timer_label = QLabel("Time: --")

    def resizeEvent(self, event) -> None:
        self.setMaximumHeight(int(self.parent().height() * 0.30))
        # self.setMaximumWidth(300)
