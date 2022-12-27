from enum import Enum


class GameMode(Enum):
    NORMAL = "Normal Go"
    SPEED = "Speed Go"


class Settings:

    GAME_MODES = tuple(GameMode)
    MIN_NUMBER_OF_PLAYERS = 2
    MAX_NUMBER_OF_PLAYERS = 4

    TIMER_START = 10
    TIMER_SPEED = 1000

    BOARD_SIZES = ["16", "13", "9", "7"]
    board_background = "./icons/board_background.jpg"

    PIECE_COLORS = [
        "#0000",
        "#000",
        "#fff",
        "#8B0000",
        "#0000FF"
    ]

    PIECE_ICONS_PATHS = [
        "./icons/empty.png",
        "icons/player_1_piece.png",
        "icons/player_2_piece.png",
        "icons/player_3_piece.png",
        "icons/player_4_piece.png"
    ]

    # stylesheets ==================================

    CURRENT_PLAYER_STYLESHEET = """
        PlayerBox{
            border: 2px solid #0000FF;
            border-radius: 5px;
            box-shadow: 0 0 10px #0000FF;
        }
        """

    SCORE_BOARD_STYLESHEET = """
        QGroupBox{
            background-color: rgba(0, 0, 0, 0.7);
        }
        QLabel{
            background-color: rgba(0, 0, 0, 0);
            color: white;
        }
        QGroupBox#first{
            border: 2px solid #0000FF;
            border-radius: 5px;
            box-shadow: 0 0 10px #0000FF;
        }
        PlayerBox{
            background-color: rgba(200, 200, 200, 0.1);
        }
        """
