from enum import Enum


class GameMode(Enum):
    NORMAL = "Normal Go"
    SPEED = "Speed Go"


class Settings:

    GAME_MODES = tuple(GameMode)
    MIN_NUMBER_OF_PLAYERS = 2
    MAX_NUMBER_OF_PLAYERS = 4
    BOARD_SIZES = ["16", "13", "9", "7"]

    TIMER_START = 10
    TIMER_SPEED = 1000
