"""
Created on 28th October 2018 by
blackat.
"""

from enum import Enum, unique


@unique
class Board(Enum):
    """
    Three different sections: Board.TODO, Board.DOING, Board.DONE.
    """
    TODO = 0
    DOING = 1
    DONE = 2
