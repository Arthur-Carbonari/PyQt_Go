import pickle

from PyQt6.QtCore import QBasicTimer
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QMessageBox, QToolTip, QFileDialog
from Board import Board
from MenuBar import GameMenuBar
from ScoreBoard import ScoreBoard
from Settings import Settings, GameMode


class Go(QMainWindow):
    """A class representing a game of Go.

    This class manages the game of Go, including the board, players, and score. It also handles UI elements such as the
    score board and menu bar.

    Attributes:
        GAME_MODE: A class attribute representing the game mode (normal or speed).
        game_over: A boolean indicating whether the game has ended.
        num_players: An integer representing the number of players in the game.
        players_names: A list of strings representing the names of the players.
        players_scores: A list of floats representing the scores of the players.
        current_player: An integer representing the index of the current player.
        pass_turn_counter: An integer representing the number of consecutive turns that have been passed.
        board: An instance of the `Board` class representing the game board.
        score_board: An instance of the `ScoreBoard` class representing the score board UI element.
        undo_stack: A list of board states representing the board states that can be undone.
        redo_stack: A list of board states representing the board states that can be redone.

    """

    GAME_MODE: GameMode = GameMode.NORMAL

    def __init__(self, player_names: list[str], board_size: int):
        """
        Initializes the game by setting up the players, the board, the score board, and the menu bar.

        :param player_names: A list of strings representing the names of the players.
        :param board_size: An integer representing the size of the board.
        """

        super().__init__()

        self.setWindowIcon(QIcon("./icons/pokeball.png"))

        # Set background color of WelcomeScreen
        self.setObjectName("Go")

        self.game_over = False
        self.num_players = len(player_names)
        self.players_names = player_names
        self.players_scores = self.get_initial_scores()

        self.current_player = 0
        self.pass_turn_counter = 0

        self.board = Board(self, board_size)

        self.score_board = ScoreBoard(self, player_names)
        self.set_score_board(self.players_scores)

        self.undo_stack = []
        self.redo_stack = []

        self.setMenuBar(GameMenuBar(self).init_menu())

        self.init_ui()

        self.set_player_turn(0)

    def init_ui(self):
        """
        Initiates the UI elements for the game.

        This method sets up the layout of the game, including the board and score board, and sets the window style and
        size.

        """

        self.setStyleSheet("""
                            Go#Go{
                                background-image: url(./icons/go_background1.jpg);
                                background-size: cover;
                                background-position: bottom right;
                                    }
                            """)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)
        main_layout.addWidget(self.board, 9)
        main_layout.addWidget(self.score_board, 2)

        screen = self.screen().availableGeometry()

        self.setMinimumWidth(int(screen.width() * 0.8))
        self.setMinimumHeight(int(screen.height() * 0.88))

        self.setWindowTitle('Go')

    def get_initial_scores(self) -> list[float]:
        """
        Gets the initial scores for each player.

        This method calculates and returns the initial scores for each player based on the number of players
        in the game.


        :return: A list of floats representing the initial scores for each player.

        """
        return [round((i != 0) * 7.5 / (2 ** (self.num_players - i - 1)), 1) for i in range(self.num_players)]

    def set_player_turn(self, player: int):
        """
        Sets the current player's turn and updates the UI to reflect the change.

        :param player: An integer representing the index of the current player in the list of player names.
        """

        if self.game_over:
            return

        self.current_player = player
        self.score_board.set_turn_player(player)
        self.board.set_player_turn(player)

    def next_turn(self):
        """
        Move to the next player's turn.

        :return: None
        """
        if self.game_over:
            return
        self.current_player = (self.current_player + 1) % self.num_players
        self.score_board.next_turn()
        self.board.set_player_turn(self.current_player)

    def pass_turn(self):
        """
        Moves to the next turn if the game is not over.

        This method increments the pass turn counter. If the counter equals the number of players, the game is finished.
        Otherwise, the next turn is taken by calling the next_turn method.
        """

        if self.game_over:
            return

        self.pass_turn_counter += 1

        if self.pass_turn_counter == self.num_players:
            self.finish_game()
            return

        self.next_turn()

    def make_move(self, piece):
        """
        Makes a move on the board by placing the given piece for the current turns' player.

        This method first checks if the move is valid. If the move is valid, it places the piece on the board, removes
        any enemy groups that have been captured, and updates the current player. If the move is not valid, it notifies
        the user.

        :param piece: The piece to be placed on the board.
        """

        if self.game_over:
            return

        board_before_move = self.board.get_current_state()

        # Check if the move is valid
        if not self.board.is_move_valid(piece.row, piece.column, self.current_player):
            QToolTip.showText(QCursor.pos(), "Invalid Move: Self capture is not allowed")
            return

        print("current player", self.current_player)
        self.board.place_piece(piece, self.current_player)

        pieces_captured = self.board.capture_surrounding_pieces(piece)

        # Check for Ko situation
        if self.is_ko_situation(piece.row, piece.column):
            # If it's a Ko situation we inform the user and reset the board to its state before the move
            QToolTip.showText(QCursor.pos(), "Invalid Move: Ko Rule")
            self.board.load_state(board_before_move)
            return

        # Add the board state at the beginning of the turn to the undo stack
        self.undo_stack.append((board_before_move, self.current_player, pieces_captured))

        # Empties the redo_stack if there was anything on there
        if self.redo_stack:
            self.redo_stack[:] = []

        # Updates the score board
        self.players_scores[self.current_player] += pieces_captured
        self.score_board.update_player_capture(self.current_player, self.players_scores[self.current_player])

        # Resets the pass turn counter
        self.pass_turn_counter = 0

        self.next_turn()

    def is_ko_situation(self, move_row, move_column):
        """
        Checks if the current move is a Ko situation.
        A ko situation occurs when a player makes a move that causes the board to return to immediate a previous state.

        :param move_row: The row of the current move.
        :param move_column: The column of the current move.
        :return: True if the current move is a ko situation, False otherwise.
        """

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

        board_state, player, pieces_captured = self.undo_stack.pop()

        self.redo_stack.append((self.board.get_current_state(), self.current_player, pieces_captured))

        self.board.load_state(board_state)

        self.set_player_turn(player)

        self.players_scores[self.current_player] -= pieces_captured
        self.score_board.update_player_capture(self.current_player, self.players_scores[self.current_player])

    def redo_move(self):
        """
        Redoes the previous move that was undone.

        This method retrieves the state of the board and current player from the top of the redo stack and applies it to
        the game.
        The current state of the board and player are then added to the undo stack to allow for future undos.
        """
        if not self.redo_stack:
            return

        board_state, player, pieces_captured = self.redo_stack.pop()

        self.undo_stack.append((self.board.get_current_state(), self.current_player, pieces_captured))

        self.board.load_state(board_state)

        self.players_scores[self.current_player] += pieces_captured
        self.score_board.update_player_capture(self.current_player, self.players_scores[self.current_player])

        self.set_player_turn(player)

    def finish_game(self):
        self.game_over = True

        controlled_territories = self.board.get_controlled_territories()

        for player_number in range(self.num_players):
            self.players_scores[player_number] += len(controlled_territories[player_number + 1])
            self.score_board.update_player_capture(player_number, self.players_scores[player_number])

        self.score_board.display_winner(self.players_scores)

    def to_dictionary(self) -> dict:
        """
        Convert the current game state to a dictionary.

        :return: A dictionary representation of the current game state, including
            the game mode, game over status, player names and scores, current
            player, pass turn counter, board size, and board array.
        """

        return {
            "game_mode": self.GAME_MODE,
            "game_over": self.game_over,
            "players_names": self.players_names,
            "players_scores": self.players_scores,
            "current_player": self.current_player,
            "pass_turn_counter": self.pass_turn_counter,
            "board_size": self.board.board_size,
            "board_array": self.board.board_array,
        }

    def save_game(self):
        """
        Save the current game state to a pickle file.

        This method opens a file save dialog to allow the user to select the
        location and filename for the pickle file. It then converts the current
        game state to a dictionary using the `to_dictionary` method and saves
        the dictionary to the pickle file using the `pickle` module.
        """

        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Pickle File (*.pkl)")

        game = self.to_dictionary()

        with open(filename, "wb", ) as file:
            pickle.dump(game, file)

    def reset_game(self):

        result = QMessageBox.question(self, "Reset Game?",
                                      "Are you sure you want to reset the current game?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                      QMessageBox.StandardButton.No)

        # Check the result of the dialog
        if result == QMessageBox.StandardButton.No:
            return

        self.reset()

    def reset(self):
        self.game_over = False
        self.pass_turn_counter = 0
        self.players_scores = self.get_initial_scores()

        self.undo_stack = []
        self.redo_stack = []

        self.board.reset()

        self.score_board.reset()

        self.set_score_board(self.players_scores)
        self.set_player_turn(0)

    def set_score_board(self, score):
        for player_number, captured_pieces in enumerate(score):
            self.score_board.update_player_capture(player_number, captured_pieces)

    @staticmethod
    def load_game_from_dictionary(game_object: dict):

        # TODO sanitize the game dict to make sure it has all the properties and they are of valid types
        go = Go(game_object["players_names"], game_object["board_size"])
        go.board.load_state(game_object["board_array"])
        go.set_score_board(game_object["players_scores"])
        go.set_player_turn(game_object["current_player"])
        go.score_board.set_turn_player(go.current_player)
        go.pass_turn_counter = game_object["pass_turn_counter"]

        if game_object["game_over"]:
            go.finish_game()

        return go


class SpeedGo(Go):
    GAME_MODE: GameMode = GameMode.SPEED

    def __init__(self, players_names, board_size, remaining_time=None):
        super().__init__(players_names, board_size)

        self.timer = QBasicTimer()

        if remaining_time is None:
            self.remaining_time = [Settings.TIMER_START] * self.num_players
        else:
            self.remaining_time = remaining_time

        for player_number, time in enumerate(self.remaining_time):
            self.score_board.update_player_time(player_number, time)

        self.timer.start(Settings.TIMER_SPEED, self)

    def next_turn(self):
        # TODO test this
        super(SpeedGo, self).next_turn()

        if self.remaining_time[self.current_player] <= 0:
            self.pass_turn()

    def finish_game(self):
        self.timer.stop()
        super().finish_game()

    def reset(self):
        super().reset()

        self.remaining_time[:] = [Settings.TIMER_START] * self.num_players

        for player_number, time in enumerate(self.remaining_time):
            self.score_board.update_player_time(player_number, time)

        if not self.timer.isActive():
            self.timer.start(Settings.TIMER_SPEED, self)

    def to_dictionary(self):
        game = super(SpeedGo, self).to_dictionary()
        game["remaining_time"] = self.remaining_time
        return game

    @staticmethod
    def load_game_from_dictionary(game_object: dict):

        # TODO sanitize the game dict to make sure it has all the properties and they are of valid types
        speed_go = SpeedGo(game_object["players_names"], game_object["board_size"], game_object["remaining_time"])
        speed_go.board.load_state(game_object["board_array"])
        speed_go.set_score_board(game_object["players_scores"])
        speed_go.set_player_turn(game_object["current_player"])
        speed_go.score_board.set_turn_player(speed_go.current_player)
        speed_go.pass_turn_counter = game_object["pass_turn_counter"]

        if game_object["game_over"]:
            speed_go.finish_game()

        return speed_go

    # EVENTS ================================================

    def timerEvent(self, event):
        """this event is automatically called when the timer is updated. based on the timer_speed variable """
        # if the timer that has 'ticked' is the one in this class
        if event.timerId() == self.timer.timerId():
            if self.remaining_time[self.current_player] == 0:
                return

            # update counter and timer label on scoreboard
            self.remaining_time[self.current_player] -= 1
            self.score_board.update_player_time(self.current_player, self.remaining_time[self.current_player])

            if self.remaining_time[self.current_player] == 0:
                self.pass_turn()
                return
        else:
            self.timerEvent(event)  # if we do not handle an event we should pass it to the super
            # class for handling
