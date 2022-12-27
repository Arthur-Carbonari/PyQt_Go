from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QPixmap, QFont
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QLineEdit, QMainWindow, \
    QRadioButton, QComboBox, QSpinBox, QButtonGroup

from Settings import Settings
from MenuBar import MenuBar


class WelcomeScreen(QMainWindow):
    Main = None

    def __init__(self):
        super().__init__()

        main_widget = QFrame()
        # default number of players
        self.player_count = 2

        self.setMenuBar(MenuBar(self).init_menu())
        # Set window title
        self.setWindowTitle("Pokemon Go")

        # Set background color of WelcomeScreen
        self.setObjectName("WelcomeScreen")
        self.background = QPixmap("./icons/welcome_background.jpg")
        self.setStyleSheet("""
                            WelcomeScreen#WelcomeScreen{
                                background-image: url(./icons/welcome_background.png);
                                background-size: cover;
                                background-position: bottom right;
                            }
                            """)

        # items that will be used later
        self.player_spinbox = QSpinBox()                # number of players comboBox
        self.name_input_box = QVBoxLayout()             # player name box
        self.name_input_fields = []                     # storage for QLineEdits
        self.board_size_cbox = QComboBox()              # board size comboBox

        # Game mode selection button group
        self.game_mode_selection = QButtonGroup()
        game_mode_radio_buttons = [QRadioButton(game_mode.value) for game_mode in Settings.GAME_MODES]
        [self.game_mode_selection.addButton(radio_button, i) for i, radio_button in enumerate(game_mode_radio_buttons)]
        self.game_mode_selection.button(0).setChecked(True)

        self.button = QPushButton("Start Game")         # start game button
        # Create the QFrame and set its size and layout
        self.frame = QFrame(self)
        self.frame.setFixedSize(int(self.width() / 1.7), int(self.height() / 1.5))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setStyleSheet('background-color: white;')
        self.main_layout = self.create_main_layout()
        self.frame.setLayout(self.main_layout)

        # Center the frame in the WelcomeScreen widget
        frame_layout = QHBoxLayout()
        frame_layout.addStretch()
        frame_layout.addWidget(self.frame)
        frame_layout.addStretch()
        main_widget.setLayout(frame_layout)

        self.setCentralWidget(main_widget)

        screen = self.screen().availableGeometry()
        self.setMinimumWidth(int(screen.width() * 0.8))
        self.setMinimumHeight(int(screen.height() * 0.88))

    def create_main_layout(self):
        main_layout = QVBoxLayout()

        # HEADER LINES
        # Welcoming header label
        label = QLabel("Welcome to Pokemon Go")
        label.setFont(QFont("serif", 14))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # add line to main layout
        main_layout.addWidget(label)

        main_layout.addSpacing(self.height()//20)

        # NUMBER OF PLAYERS LINE
        no_of_players = self.create_number_of_players_line()
        # add line to main layout
        main_layout.addLayout(no_of_players)

        # PLAYER NAME LINES
        # Create the player name input fields and labels and add them to name input box
        for i in range(self.player_count):
            name_input_line = QHBoxLayout()
            # label
            name_label = QLabel("Player " + str(i + 1) + ": ")
            # input area
            name_input = QLineEdit()
            self.name_input_fields.append(name_input)
            name_input.setPlaceholderText("Player " + str(i + 1))
            # add label and input area in a line
            name_input_line.addWidget(name_label)
            name_input_line.addWidget(name_input)
            # add line to name input box
            self.name_input_box.addLayout(name_input_line)

        # add box to main layout
        main_layout.addStretch()
        main_layout.addLayout(self.name_input_box)
        main_layout.addStretch()

        # BOARD SIZE LINE
        board_size = self.create_board_size_line()
        # add line to main layout
        main_layout.addLayout(board_size)

        # PLAY MODE SELECTION LINE
        # Create play mode radio buttons and add them to layout
        game_mode = self.create_game_mode_line()
        # add line to main layout
        main_layout.addLayout(game_mode)

        # START GAME BUTTON LINE
        # Add start game button to the main layout
        main_layout.addStretch()
        main_layout.addWidget(self.button)

        return main_layout

    def create_board_size_line(self):
        # create line layout
        layout = QHBoxLayout()
        # label
        layout.addWidget(QLabel("Board size: "))
        # populate combo box
        self.board_size_cbox.addItems(Settings.BOARD_SIZES)
        # add combo box to line
        layout.addWidget(self.board_size_cbox)

        return layout

    def create_number_of_players_line(self):
        # create line layout
        layout = QHBoxLayout()
        # create label and add to line
        layout.addWidget(QLabel("Number of players: "))
        # set range of spinbox
        self.player_spinbox.setMinimum(Settings.MIN_NUMBER_OF_PLAYERS)
        self.player_spinbox.setMaximum(Settings.MAX_NUMBER_OF_PLAYERS)
        # connect to set_number_of_players method
        self.player_spinbox.valueChanged.connect(self.change_number_of_players)
        # add combo box to line
        layout.addWidget(self.player_spinbox)

        return layout

    def create_game_mode_line(self):
        # create layout
        layout = QHBoxLayout()
        # label
        layout.addWidget(QLabel("Mode: "))
        [layout.addWidget(button) for button in self.game_mode_selection.buttons()]

        return layout

    def add_name_input_lines(self):

        for player in range(self.player_count):
            # create a line layout
            player_layout = QHBoxLayout()
            # create label and add layout
            player_layout.addWidget(QLabel("Player " + str(player + 1) + ": "))
            # input area
            player_input = QLineEdit()
            player_input.setPlaceholderText("Player " + str(player + 1) + " name")
            # add input area to line
            player_layout.addWidget(player_input)
            # add input area to list
            self.name_input_fields.append(player_input)
            # add line layout to VBox
            self.name_input_box.addLayout(player_layout)

    def delete_name_input_lines(self):
        for i in range(1, self.player_count + 1):
            # get the last layout inside the VBox
            item = self.name_input_box.itemAt(self.name_input_box.count() - i)
            # delete every item inside the line layout
            for ele in range(item.count()):
                item.itemAt(ele).widget().deleteLater()
            # delete the item
            item.deleteLater()

        # clear list
        self.name_input_fields.clear()

    def change_number_of_players(self):
        """
        Adds or removes inputs field for player names from the welcome window form
        """
        self.delete_name_input_lines()
        self.player_count = int(self.player_spinbox.value())
        self.add_name_input_lines()

    # EVENTS
    # def paintEvent(self, event):
    #     """paints the board and the pieces of the game"""
    #
    #     painter = QPainter(self)
    #     # Draws the board background
    #     self.background = self.background.scaled(self.width(), self.height())
    #     painter.drawPixmap(QPoint(), self.background)
