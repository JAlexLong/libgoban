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


@dataclass
class Player:
    name: str
    stone: Optional[Stone] = None

@dataclass
class Move:
    point: Point
    stone: Stone

    def islegal(self, board: Board): ...

@ dataclass
class Game:
    player1: Player
    player2: Player
    turn: Stone = Stone.BLACK
    board: Board = Board()
    history: list = []

    def make_move(self, move: Move):
        """Makes move in self.Board, self.history and changes self.turn"""
        col, row = move.point
        # if self.move_is_legal(move, self.board):
        self.board[col][row] = move.stone
        self.history.append(move)
        self.turn = self.turn.opposite_color()
        #else:
        #    raise ValueError(f"The move {move} ")

    def undo_last_move(self):
        last_move = self.history.pop()
        self.remove_stone(last_move)
        self.turn = self.turn.opposite_color()
