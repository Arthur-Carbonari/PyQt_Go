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

    def __init__(self, player_names):
        super().__init__()

        # TODO: also if timed mode is deactivated count upwards to see how long to make move
        self.is_timed_mode_on = True    # Speed go mode, change this to deactivate game over with timer
        self.game_over = False  # TODO: when true seize all operations, merge it with previous one

        # TODO: will be made more flexible
        player_names = player_names if len(player_names) != 0 else ["Black", "White"]
        self.score_board = ScoreBoard(self, player_names)
        self.board = Board(self)
        self.num_players = 2
        self.current_player = 1

        self.undo_stack = []
        self.redo_stack = []

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

    def make_move(self, piece):
        """
        Makes a move on the board by placing the given piece for the current turns player.

        This method first checks if the move is valid. If the move is valid, it places the piece on the board, removes
        any enemy groups that have been captured, and updates the current player. If the move is not valid, it notifies
        the user. TODO: change from printing error message to something in the UI

        :param piece: The piece to be placed on the board.
        """

        board_before_move = self.board.get_current_state()

        # Check if the move is valid
        if not self.board.is_move_valid(piece.row, piece.column, self.current_player):
            print("Invalid Move")
            return

        self.board.place_piece(piece, self.current_player)

        self.board.capture_surrounding_pieces(piece)

        # Check for Ko situation
        if self.is_ko_situation(piece.row, piece.column):
            # If it's a Ko situation we inform the user and reset the board to its state before the move
            print("Invalid move, Ko situation")
            self.board.load_state(board_before_move)
            return

        # Add the board state at the beginning of the turn to the undo stack
        self.undo_stack.append((board_before_move, self.current_player))

        # Empties the redo_stack if there was anything on there
        if self.redo_stack:
            self.redo_stack[:] = []

        self.next_turn()

    def is_ko_situation(self, move_row, move_column):

        # Check if there has been a previous state, if not then it's not a ko situation
        if not self.undo_stack:
            return False

        # We get the new proposed board state
        new_board_state = self.board.get_current_state()

        number_of_turns = len(self.undo_stack)
        # if this is true that means that this is the first turn of the current player, therefore Ko is impossible
        if number_of_turns < self.num_players:
            return False

        # Now get the board state at the end of the current player last turn
        previous_board_state = self.undo_stack[number_of_turns - self.num_players + 1][0]

        # If at the player move is not retaking a square he lost since the previous turn we return false
        if new_board_state[move_row][move_column] != previous_board_state[move_row][move_column]:
            return False

        # Now if the move doesn't result in a repeat of previous game state we return false
        if new_board_state != previous_board_state:
            return False

        # Now if it repeats a previous board state we return true
        return True

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

        self.redo_stack.append((self.board.get_current_state(), self.current_player))

        board_state, player = self.undo_stack.pop()
        self.board.load_state(board_state)
        self.current_player = player

    def redo_move(self):
        """
        Redoes the previous move that was undone.

        This method retrieves the state of the board and current player from the top of the redo stack and applies it to
        the game.
        The current state of the board and player are then added to the undo stack to allow for future undos.
        """
        if not self.redo_stack:
            return

        self.undo_stack.append((self.board.get_current_state(), self.current_player))

        board_state, player = self.redo_stack.pop()
        self.board.load_state(board_state)
        self.current_player = player

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
        if self.undo_stack:
            self.board.reset()

        # reset the score board
        # self.score_board.reset()

        self.current_player = 1
        self.score_board.reset()


class GameMenuBar(MenuBar):

    def __init__(self, game_window: Go):
        super().__init__(game_window)

        # GAME MENU

        # Reset Game Action
        self.reset_game_action = QAction(QIcon("./icons/save.png"), "Reset Game", game_window)
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
        self.undo_action.triggered.connect(game_window.undo_move)

        # Redo Action
        self.redo_action = QAction(QIcon("./icons/save.png"), "Redo Move", game_window)
        self.redo_action.setShortcut("Ctrl+Y")
        self.redo_action.triggered.connect(game_window.redo_move)

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
