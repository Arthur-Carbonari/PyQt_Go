from enum import Enum


class GameMode(Enum):
    NORMAL = "Normal Go"
    SPEED = "Speed Go"


class Settings:

    GAME_MODES = tuple(GameMode)

    TIMER_START = 10
    TIMER_SPEED = 1000
