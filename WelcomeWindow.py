from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QPixmap, QFont
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QLineEdit, QMainWindow, QRadioButton, \
    QComboBox

from MenuBar import MenuBar


class WelcomeScreen(QMainWindow):
    Main = None

    # TODO: add size of board, player no 2 or 4, timed or normal
    def __init__(self):
        super().__init__()

        main_widget = QFrame()
        # default number of players
        self.player_count = 2

        self.setMenuBar(MenuBar(self).init_menu())
        self.setWindowTitle("Welcome to Pokemon Go")
        # Set background color of WelcomeScreen
        self.setObjectName("WelcomeScreen")
        self.background = QPixmap("./icons/welcome_background.jpg")

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
        layout = QVBoxLayout()

        # Welcoming header label
        label = QLabel("Welcome to Pokemon Go")
        label.setFont(QFont("serif", 14))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()

        # Create the player name input fields and labels and add them to layout
        for i in range(self.player_count):
            player_layout = QHBoxLayout()
            player_label = QLabel("Player " + str(i + 1) + ": ")
            player_input = QLineEdit()
            player_input.setPlaceholderText("Player " + str(i + 1))
            player_layout.addWidget(player_label)
            player_layout.addWidget(player_input)
            layout.addStretch()
            layout.addLayout(player_layout)
            layout.addStretch()

        # Create player number option radio buttons and add them to layout
        no_of_players = QHBoxLayout()
        layout.addStretch()
        layout.addLayout(no_of_players)
        layout.addStretch()
        no_of_players.addWidget(QLabel("Number of players"))
        self.player_option_cbox = QComboBox()
        self.player_option_cbox.addItems(["2", "4"])
        self.player_option_cbox.currentIndexChanged.connect(self.set_number_of_players)
        no_of_players.addWidget(self.player_option_cbox)

        # Create play mode radio buttons and add them to layout
        play_mode = QHBoxLayout()
        layout.addStretch()
        layout.addLayout(play_mode)
        layout.addStretch()
        play_mode.addWidget(QLabel("Mode: "))
        modes = ["Normal Go", "Speed Go"]
        for i in range(2):
            string = modes[i]
            self.mode = QRadioButton(string)
            self.mode.value = i
            play_mode.addWidget(self.mode)

        # Create button, add them to the layout
        self.button = QPushButton("Start Game")
        layout.addStretch()
        layout.addWidget(self.button)

        return layout

    def set_number_of_players(self):
        # will add more Qline to layout
        sender = self.sender()
        self.player_count = sender.currentText()

    # EVENTS
    def paintEvent(self, event):
        """paints the board and the pieces of the game"""

        painter = QPainter(self)
        # Draws the board background
        self.background = self.background.scaled(self.width(), self.height())
        painter.drawPixmap(QPoint(), self.background)
