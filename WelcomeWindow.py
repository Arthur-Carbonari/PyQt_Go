from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QPixmap, QFont
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QLineEdit, QMainWindow, QRadioButton, \
    QComboBox

from MenuBar import MenuBar


class WelcomeScreen(QMainWindow):
    Main = None
    player_options = ["2", "3", "4"]
    board_sizes = ["7", "9", "13", "16"]

    def __init__(self):
        super().__init__()

        main_widget = QFrame()
        # default number of players
        self.player_count = 2

        self.setMenuBar(MenuBar(self).init_menu())
        # Set window title
        self.setWindowTitle("Welcome to Pokemon Go")

        # Set background color of WelcomeScreen
        self.setObjectName("WelcomeScreen")
        self.background = QPixmap("./icons/welcome_background.jpg")

        # items that will be used later
        self.name_input_box = QVBoxLayout()       # player name box
        self.name_input_fields = []                 # storage for QLineEdits
        self.player_option_cbox = QComboBox()       # number of players comboBox
        self.board_size_cbox = QComboBox()               # board size comboBox
        self.mode = QRadioButton()                  # game mode radioButton
        self.button = QPushButton("Start Game")     # start game button

        # Create the QFrame and set its size and layout
        self.frame = QFrame(self)
        self.frame.setFixedSize(int(self.width() / 2), int(self.height() / 2))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setStyleSheet('background-color: white;')
        self.main_layout = self.update_main_layout()
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

    def update_main_layout(self):
        main_layout = QVBoxLayout()

        # HEADER LINES
        # Welcoming header label
        label = QLabel("Welcome to Pokemon Go")
        label.setFont(QFont("serif", 14))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # add line to main layout
        main_layout.addStretch()
        main_layout.addWidget(label)
        main_layout.addStretch()

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


        # NUMBER OF PLAYERS LINE
        # create line layout
        no_of_players = QHBoxLayout()
        # create label and add to line
        no_of_players.addWidget(QLabel("Number of players: "))
        # populate combo box
        self.player_option_cbox.addItems(self.player_options)
        # connect to set_number_of_players method
        self.player_option_cbox.currentIndexChanged.connect(self.set_number_of_players)
        # add combo box to line
        no_of_players.addWidget(self.player_option_cbox)
        # add line to main layout
        main_layout.addStretch()
        main_layout.addLayout(no_of_players)
        main_layout.addStretch()

        # BOARD SIZE LINE
        # create line layout
        board_size_line = QHBoxLayout()
        # label
        board_size_line.addWidget(QLabel("Board size: "))
        # populate combo box
        self.board_size_cbox.addItems(self.board_sizes)
        # add combo box to line
        board_size_line.addWidget(self.board_size_cbox)
        # add line to main layout
        main_layout.addStretch()
        main_layout.addLayout(board_size_line)
        main_layout.addStretch()


        # PLAY MODE SELECTION LINE
        # Create play mode radio buttons and add them to layout
        play_mode = QHBoxLayout()
        main_layout.addStretch()
        main_layout.addLayout(play_mode)
        main_layout.addStretch()
        play_mode.addWidget(QLabel("Mode: "))
        modes = ["Normal Go", "Speed Go"]
        for i in range(2):
            string = modes[i]
            self.mode = QRadioButton(string)
            # toggle first option
            # if i == 0: self.mode.toggle()
            self.mode.value = i
            play_mode.addWidget(self.mode)

        # START GAME BUTTON LINE
        # Add start game button to the main layout
        main_layout.addStretch()
        main_layout.addWidget(self.button)

        return main_layout

    def set_number_of_players(self):
        """sets current player with change of dropbox"""
        # TODO: will add more QLineEdit to layout
        self.player_count = self.sender().currentText()

    # EVENTS
    def paintEvent(self, event):
        """paints the board and the pieces of the game"""

        painter = QPainter(self)
        # Draws the board background
        self.background = self.background.scaled(self.width(), self.height())
        painter.drawPixmap(QPoint(), self.background)
