import os
import pickle

from PyQt6.QtWidgets import QApplication, QMessageBox, QFileDialog
import sys

from Go import Go, SpeedGo
from MenuBar import MenuBar
from Settings import Settings, GameMode
from WelcomeWindow import WelcomeScreen


class Main:

    def __init__(self):

        MenuBar.Main = self
        WelcomeScreen.Main = self
        self.player_names = []

        self.current_window = WelcomeScreen()
        self.connect_ws()
        self.current_window.show()

    def show_game_screen(self):
        players_name = []

        for player_number, name_field in enumerate(self.current_window.name_input_fields):

            player_name: str = name_field.text()
            if player_name == '' or player_name.isspace():
                player_name = "Player " + str(player_number + 1)

            players_name.append(player_name)

        board_size = int(self.current_window.board_size_cbox.currentText())
        game_mode = Settings.GAME_MODES[self.current_window.game_mode_selection.checkedId()]

        if game_mode == GameMode.SPEED:
            print("speed")
            go = SpeedGo(players_name, board_size)
        else:
            go = Go(players_name, board_size)

        self.change_current_window(go)

    def show_welcome_screen(self):

        if isinstance(self.current_window, Go):
            # Display the confirmation dialog
            result = QMessageBox.question(self.current_window, "New Game?",
                                          "Are you sure you want to start a new game?",
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                          QMessageBox.StandardButton.No)

            # Check the result of the dialog
            if result == QMessageBox.StandardButton.No:
                return

        welcome_screen = WelcomeScreen()

        self.change_current_window(welcome_screen)
        self.connect_ws()

    def change_current_window(self, new_window):
        self.current_window.hide()
        self.current_window.close()
        self.current_window = new_window
        self.current_window.show()

    def load_game(self):
        file_name, _ = QFileDialog.getOpenFileName(self.current_window, "Open File", "", "Pickle File (*.pkl)")

        if not os.path.exists(file_name):
            return None

        with open(file_name, "rb") as f:
            # Load the object from the file
            game_object = pickle.load(f)

        game_mode = game_object["game_mode"]

        if not game_mode:
            return

        if game_mode == GameMode.SPEED:
            new_game = SpeedGo.load_game_from_dictionary(game_object)
        else:
            new_game = Go.load_game_from_dictionary(game_object)

        if new_game is None:
            return

        self.change_current_window(new_game)

    def change_board_background(self):
        print("Change board background")

    def show_help_dialog(self):
        print("Show help dialog")
        dlg = QMessageBox(self.current_window)
        dlg.setWindowTitle("Help")
        dlg.setWindowModality(self.current_window.windowModality().NonModal)
        dlg.setIcon(dlg.icon().Information)

        dlg.setText("""
                Click on board intersections to put a piece.
                If you encircle a piece you capture it.
                
                You can't put a piece where every adjacent place surrounded.
                
                for more information about rules please visit:
                    https://www.britgo.org/intro/intro2.html
                """)
        dlg.show()

    def show_about_dialog(self):
        print("Show about dialog")
        dlg = QMessageBox(self.current_window)
        dlg.setWindowTitle("About")
        dlg.setWindowModality(self.current_window.windowModality().NonModal)
        dlg.setIcon(dlg.icon().Information)

        dlg.setText("A python go game by Arthur Carbonari Martins and Mert BEKAR")
        dlg.setInformativeText("as HGP Group project 2022")
        dlg.show()

    def exit(self):
        result = QMessageBox.question(self.current_window, "Exit Game?",
                                      "Are you sure you want to exit the game?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                      QMessageBox.StandardButton.No)

        # Check the result of the dialog
        if result == QMessageBox.StandardButton.No:
            return

        exit(0)

    def connect_ws(self):
        self.current_window.button.clicked.connect(self.show_game_screen)


def main():
    app = QApplication([])
    _main = Main()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
