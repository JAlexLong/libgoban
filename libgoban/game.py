# Copyright (C) 2025  J. Alex Long <jalexlong@proton.me>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .board import Stone, Point, Board

from dataclasses import dataclass
from typing import Optional


# +-----------------+
# |  PLAYER CLASS   |
# +-----------------+

class Player:
    def __init__(self, name: str, stone: Stone):
        self.name = name
        self.stone = stone


# +-----------------+
# |  ENGINE CLASS   |
# +-----------------+

class Engine:
    def __init__(self, name: str, stone: Stone):
        self.name = name
        self.stone = stone
    
    def generate_random_move(): ...


# +-----------------+
# |   MOVE CLASS   |
# +-----------------+

@dataclass
class Move:
    point: Optional[Point]  # None represents a pass move
    stone: Stone

    def islegal(self, board: Board) -> bool: 
        if self.point == None:
            return True
        # if empty, let's place it. Obviously not final behavior
        elif isinstance(board[self.point], type(None)):
            return True
        # assume failure
        else:
            return False
        

# +------------------------+
# |   CUSTOM GAME ERRORS   |
# +------------------------+

class TurnError(ValueError):
    """Raise when a Player/Engine attempts to make a move on the wrong turn."""

class IllegalMoveError(ValueError):
    """Raise when a Player/Engine attempts to make an illegal move."""


# +-----------------+
# |   GAME CLASS   |
# +-----------------+

class Game:
    """A class representing a game of Go between two players."""
    def __init__(self, 
                 player1: Player, 
                 player2: Player, 
                 board: Board = Board(19),
                 turn: Stone = Stone.BLACK, 
                 history: list[Move] = [],
                 komi: float = 7.5,
                 captures: dict = {Stone.BLACK: 0,Stone.WHITE: 0},
                 ): 
        self.player1 = player1 
        self.player2 = player2 
        self.board = board
        self.turn = turn 
        self.history = history
        self.komi = komi
        self.captures = captures
        self.playing = False

    def make_move(self, move: Move):
        """Makes move in self.board, self.history and changes self.turn"""
        # if our move isn't a pass (i.e. move.point == None)
        self.board[move.point] = move.stone
        self.history.append(move)
        self.turn = self.turn.OTHER
        #else:
        #    raise ValueError(f"The move {move} ")

    def undo_last_move(self):
        last_move = self.history.pop()
        # TODO: implement check if last move was a 
        #       capture and restore the captured group/stone.
        self.remove_stone(last_move.point)
        self.turn = self.turn.opposite_color()

    def end(self): 
        self.playing = False

    def play(self):
        self.playing = True
