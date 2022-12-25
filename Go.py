from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QMessageBox
from Board import Board
from MenuBar import MenuBar
from ScoreBoard import ScoreBoard


class Go(QMainWindow):
    player_changed_signal = pyqtSignal(int)  # signal sent when player changed

    # Python inability to handle circular imports and then justifying it by calling it a bad design patter, is the
    # epitome of everything wrong with python and with python devs

    def __init__(self):
        super().__init__()

        # TODO: also if timed mode is deactivated count upwards to see how long to make move
        self.is_timed_mode_on = True    # Speed go mode, change this to deactivate game over with timer
        self.game_over = False  # TODO: when true seize all operations, merge it with previous one

        # TODO: will be made more flexible
        player_names = ["Black", "White"]
        self.score_board = ScoreBoard(self, player_names)
        self.board = Board(self)
        self.num_players = 2
        self.current_player = 1

        self.setMenuBar(GameMenuBar(self).init_menu())

        self.init_ui()

    def get_score_board(self):
        return self.score_board

    def init_ui(self):
        """initiates application UI"""

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)
        main_layout.addWidget(self.board, 9)
        main_layout.addWidget(self.score_board, 2)

        self.score_board.make_connection(self.board)

        screen = self.screen().availableGeometry()

        self.setMinimumWidth(int(screen.width() * 0.8))
        self.setMinimumHeight(int(screen.height() * 0.88))

        self.setWindowTitle('Go')

    def next_turn(self):
        self.current_player = (self.current_player % self.num_players) + 1
        self.score_board.change_player(self.current_player - 1)
        # TODO: dont reset, change it to the next player, the timer will be accumulative it wont reset on turn pass,
        #  just like in chess

    def finish_game(self):
        self.game_over = True  # GAME OVER

    def save_game(self):
        print("Save the current state of the game to a file")

    def reset_game(self):

        result = QMessageBox.question(self, "Reset Game?",
                                      "Are you sure you want to reset the current game?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                      QMessageBox.StandardButton.No)

        # Check the result of the dialog
        if result == QMessageBox.StandardButton.No:
            return

        # If this is false that means that no move has been made so no need to reset the board
        if self.board.undo_stack:
            self.board.reset()

        # reset the score board
        # self.score_board.reset()

        self.current_player = 1


class GameMenuBar(MenuBar):

    def __init__(self, game_window: Go):
        super().__init__(game_window)

        # GAME MENU

        # Reset Game Action
        self.reset_game_action = QAction(QIcon("./icons/save.png"), "Load Game", game_window)
        self.reset_game_action.setShortcut("Ctrl+R")
        self.reset_game_action.triggered.connect(game_window.reset_game)

        # Save Game Action
        self.save_game_action = QAction(QIcon("./icons/save.png"), "Save Game", game_window)
        self.save_game_action.setShortcut("Ctrl+S")
        self.save_game_action.triggered.connect(game_window.save_game)

        # ACTIONS MENU

        # Undo Action
        self.undo_action = QAction(QIcon("./icons/save.png"), "Undo Move", game_window)
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.triggered.connect(game_window.board.undo_move)

        # Redo Action
        self.redo_action = QAction(QIcon("./icons/save.png"), "Redo Move", game_window)
        self.redo_action.setShortcut("Ctrl+Y")
        self.redo_action.triggered.connect(game_window.board.redo_move)

    def init_menu(self):
        # Add menus to menu bar
        game_menu = self.addMenu("&Game")
        actions_menu = self.addMenu("&Actions")
        window_menu = self.addMenu("&Window")
        help_menu = self.addMenu("&Help")

        # Add actions to menus
        game_menu.addAction(self.reset_game_action)
        game_menu.addAction(self.new_game_action)
        game_menu.addAction(self.save_game_action)
        game_menu.addAction(self.load_game_action)
        game_menu.addAction(self.exit_action)

        actions_menu.addAction(self.undo_action)
        actions_menu.addAction(self.redo_action)

        window_menu.addAction(self.change_background_action)

        help_menu.addAction(self.help_action)
        help_menu.addAction(self.about_action)

        return self
