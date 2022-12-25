from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QLineEdit, QMainWindow

from MenuBar import MenuBar


class WelcomeScreen(QMainWindow):

    Main = None

    def __init__(self):
        super().__init__()

        main_widget = QFrame()

        self.setMenuBar(MenuBar(self).init_menu())

        # Set background color of WelcomeScreen
        self.setStyleSheet('background-color: lightgray;')

        # Create the QFrame and set its size and layout
        self.frame = QFrame(self)
        self.frame.setFixedSize(int(self.width() / 1.8), int(self.height() / 1.4))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setStyleSheet('background-color: white;')
        layout = QVBoxLayout()
        self.frame.setLayout(layout)

        # Create button, add them to the layout
        self.button = QPushButton("Start")
        self.button.clicked.connect(self.Main.show_game_screen)

        # Create player 1 and player 2 input fields
        self.player1_input = QLineEdit()
        self.player1_input.setPlaceholderText("Player 1")
        self.player2_input = QLineEdit()
        self.player2_input.setPlaceholderText("Player 2")

        label = QLabel("Welcome")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()

        # Create the player name input fields and labels
        player1_layout = QHBoxLayout()
        player1_label = QLabel("Player 1:")
        self.player1_input = QLineEdit()
        self.player1_input.setPlaceholderText("Player 1")
        player1_layout.addWidget(player1_label)
        player1_layout.addWidget(self.player1_input)
        layout.addLayout(player1_layout)

        player2_layout = QHBoxLayout()
        player2_label = QLabel("Player 2:")
        self.player2_input = QLineEdit()
        self.player2_input.setPlaceholderText("Player 2")
        player2_layout.addWidget(player2_label)
        player2_layout.addWidget(self.player2_input)
        layout.addLayout(player2_layout)
        layout.addStretch()

        layout.addWidget(self.button)

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

