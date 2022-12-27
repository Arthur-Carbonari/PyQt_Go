import os.path
import pickle

from PyQt6.QtCore import pyqtSignal, QBasicTimer
from PyQt6.QtGui import QAction, QIcon, QCursor
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QMessageBox, QToolTip, QFileDialog
from Board import Board
from MenuBar import MenuBar
from ScoreBoard import ScoreBoard
from Settings import Settings


class Go(QMainWindow):
    player_changed_signal = pyqtSignal(int)  # signal sent when player changed

    def __init__(self, player_names: list[str], board_size: int):
        super().__init__()

        # TODO: also if timed mode is deactivated count upwards to see how long to make move
        self.is_timed_mode_on = True    # Speed go mode, change this to deactivate game over with timer
        self.game_over = False  # TODO: when true seize all operations, merge it with previous one

        self.players_names = player_names

        self.board = Board(self, board_size)
        self.score_board = ScoreBoard(self, player_names)
        self.num_players = len(player_names)
        self.current_player = 1

        self.players_captured_pieces = [0] * self.num_players

        self.pass_turn_counter = 0

        self.undo_stack = []
        self.redo_stack = []

        self.setMenuBar(GameMenuBar(self).init_menu())

        self.init_ui()

    def init_ui(self):
        """initiates application UI"""

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)
        main_layout.addWidget(self.board, 9)
        main_layout.addWidget(self.score_board, 2)

        screen = self.screen().availableGeometry()

        self.setMinimumWidth(int(screen.width() * 0.8))
        self.setMinimumHeight(int(screen.height() * 0.88))

        self.setWindowTitle('Go')

    def next_turn(self):
        self.current_player = (self.current_player % self.num_players) + 1
        self.score_board.change_player(self.current_player)

    def pass_turn(self):
        self.pass_turn_counter += 1

        if self.pass_turn_counter >= self.num_players:
            self.finish_game()
            return

        self.next_turn()

    def make_move(self, piece):
        """
        Makes a move on the board by placing the given piece for the current turns player.

        This method first checks if the move is valid. If the move is valid, it places the piece on the board, removes
        any enemy groups that have been captured, and updates the current player. If the move is not valid, it notifies
        the user. TODO: change from printing error message to something in the UI

        :param piece: The piece to be placed on the board.
        """

        if self.game_over:
            return

        board_before_move = self.board.get_current_state()

        # Check if the move is valid
        if not self.board.is_move_valid(piece.row, piece.column, self.current_player):
            QToolTip.showText(QCursor.pos(), "Invalid Move: Self capture is not allowed")
            return

        self.board.place_piece(piece, self.current_player)

        pieces_captured = self.board.capture_surrounding_pieces(piece)

        # Check for Ko situation
        if self.is_ko_situation(piece.row, piece.column):
            # If it's a Ko situation we inform the user and reset the board to its state before the move
            QToolTip.showText(QCursor.pos(), "Invalid Move: Ko Rule")
            self.board.load_state(board_before_move)
            return

        # Add the board state at the beginning of the turn to the undo stack
        self.undo_stack.append((board_before_move, self.current_player))

        # Empties the redo_stack if there was anything on there
        if self.redo_stack:
            self.redo_stack[:] = []

        # Updates the score board
        self.players_captured_pieces[self.current_player - 1] += pieces_captured
        self.score_board.update_player_capture(self.current_player,
                                               self.players_captured_pieces[self.current_player - 1])

        # Resets the pass turn counter
        self.pass_turn_counter = 0

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
        print("game over")
        # TODO: Calculate final points by territory
        # TODO: Display game over message
        # TODO: Highlight winner

    def save_game(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Pickle File (*.pkl)")

        print(filename)

        game = {
            "players_name": self.players_names,
            "current_player": self.current_player,
            "board_size": self.board.board_size,
            "board_array": self.board.board_array,
        }

        with open(filename, "wb",) as file:
            pickle.dump(game, file)

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

    @staticmethod
    def load_game_from_file(file_name: str):

        if not os.path.exists(file_name):
            return None

        with open(file_name, "rb") as f:
            # Load the object from the file
            game = pickle.load(f)

        # TODO sanitize the game dict to make sure it has all the properties and they are of valid types
        go = Go(game["players_name"], game["board_size"])
        go.current_player = game["current_player"]
        go.board.load_state(game["board_array"])

        return go


class SpeedGo(Go):

    def __init__(self, players_names, board_size):
        super().__init__(players_names, board_size)

        self.timer = QBasicTimer()
        self.remaining_time = [Settings.TIMER_START] * self.num_players
        self.timer.start(Settings.TIMER_SPEED, self)

    def finish_game(self):
        self.timer.stop()
        super().finish_game()

    # EVENTS ================================================

    def timerEvent(self, event):
        """this event is automatically called when the timer is updated. based on the timer_speed variable """
        # if the timer that has 'ticked' is the one in this class
        if event.timerId() == self.timer.timerId():
            if self.remaining_time[self.current_player - 1] == 0:
                self.pass_turn()
                return

            # update counter and timer label on scoreboard
            self.remaining_time[self.current_player - 1] -= 1
            self.score_board.update_player_time(self.current_player, self.remaining_time[self.current_player - 1])
            # self.timer_labels[self.current_player].setText("Time: " + str(self.remaining_time[self.current_player]))
            # self.set_time_remaining()
        else:
            self.timerEvent(event)  # if we do not handle an event we should pass it to the super
            # class for handling


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
