from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMenuBar


class MenuBar(QMenuBar):

    Main = None

    def __init__(self, main_window):
        super().__init__()

        # GAME MENU

        # New Game Action
        self.new_game_action = QAction(QIcon("./icons/save.png"), "New Game", main_window)
        self.new_game_action.setShortcut("Ctrl+N")
        self.new_game_action.triggered.connect(self.Main.show_welcome_screen)

        # Load Game Action
        self.load_game_action = QAction(QIcon("./icons/save.png"), "Load Game", main_window)
        self.load_game_action.setShortcut("Ctrl+O")
        self.load_game_action.triggered.connect(self.Main.load_game)

        # Exit action
        self.exit_action = QAction(QIcon("./icons/exit.png"), "Exit", main_window)
        self.exit_action.setShortcut("Alt+X")
        self.exit_action.triggered.connect(self.Main.exit)

        # WINDOW MENU

        # Change Board Background
        self.change_background_action = QAction(QIcon("./icons/exit.png"), "Change Board Background", main_window)
        self.change_background_action.triggered.connect(self.Main.change_board_background)

        # HELP MENU

        # Help
        self.help_action = QAction(QIcon(), "Help", main_window)
        self.help_action.setShortcut("Ctrl+Shift+H")
        self.help_action.triggered.connect(self.Main.show_help_dialog)

        # About
        self.about_action = QAction(QIcon(), "About", main_window)
        self.about_action.setShortcut("Ctrl+Shift+A")
        self.about_action.triggered.connect(self.Main.show_about_dialog)

    def init_menu(self):

        # Add menus to menu bar
        game_menu = self.addMenu("&Game")
        window_menu = self.addMenu("&Window")
        help_menu = self.addMenu("&Help")

        # Add actions to menus
        game_menu.addAction(self.new_game_action)
        game_menu.addAction(self.load_game_action)
        game_menu.addAction(self.exit_action)

        window_menu.addAction(self.change_background_action)

        help_menu.addAction(self.help_action)
        help_menu.addAction(self.about_action)

        return self


class GameMenuBar(MenuBar):

    def __init__(self, game_window):
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