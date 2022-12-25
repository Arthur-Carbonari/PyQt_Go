from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import QApplication, QMessageBox
import sys

from go import Go
from menu_bar import MenuBar
from welcome_screen import WelcomeScreen


class Main:

    def __init__(self):

        MenuBar.Main = self
        WelcomeScreen.Main = self

        self.current_window = WelcomeScreen()
        self.current_window.show()

    def show_game_screen(self):
        go = Go()

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

    def change_current_window(self, new_window):
        self.current_window.hide()
        self.current_window.close()
        self.current_window = new_window
        self.current_window.show()

    def load_game(self):
        print("Load game object from saved games folder")

    def change_board_background(self):
        print("Change board background")

    def show_help_dialog(self):
        print("Show help dialog")

    def show_about_dialog(self):
        print("Show about dialog")

    def exit(self):
        result = QMessageBox.question(self.current_window, "Exit Game?",
                                      "Are you sure you want to exit the game?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                      QMessageBox.StandardButton.No)

        # Check the result of the dialog
        if result == QMessageBox.StandardButton.No:
            return

        exit(0)


def main():
    app = QApplication([])
    _main = Main()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()