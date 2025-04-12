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

from dataclasses import dataclass
from enum import IntEnum
from functools import lru_cache
from typing import Optional, Tuple

BOARD_LETTERS = "ABCDEFGHJKLMNOPQRST"


# +-----------------+
# |   STONE CLASS   |
# +-----------------+

class Stone(IntEnum):
    """Represents the colors of stones in the game of Go."""
    BLACK = 0
    WHITE = 1

    @property
    def OTHER(self) -> 'Stone':
        """Returns the opposite color of the current stone."""
        return Stone((Stone.WHITE.value, Stone.BLACK.value)[self.value])


# +-----------------+
# |   POINT CLASS   |
# +-----------------+

class Point(Tuple[int, int]):
    """Represents a point on a Go board."""
    def __new__(cls, col: int, row: int) -> 'Point':
        """
        Returns a new Point instance.

        Args:
            col: Column coordinate (1-indexed).
            row: Row coordinate (1-indexed).

        Returns:
            A new Point instance.
        """
        return super().__new__(cls, (col, row))

    @lru_cache(maxsize=19)
    def _col_letter_to_index(letter):
        """Converts a column letter to its 1-based index."""
        index = ord(letter) - ord('A') + 1
        if letter >= 'I':
            index -= 1
        return index

    @classmethod
    def from_str(cls, point_str: str) -> 'Point':
        """
        Returns a new Point instance from a string representation.

        Args:
            point_str: String representation of the point in the 'A1' format
                       or '1-1' format.
                       For more information, see https://senseis.xmp.net/?Coordinates

        Returns:
            A new Point instance.

        Raises:
            TypeError: If point_str is not a string.
            ValueError: If point_str fails input validation checks.
        """
        if not isinstance(point_str, str):
            raise TypeError(f"Expected a str, got {type(point_str)}")

        try:
            if len(point_str) in [2, 3] and not '-' in point_str:
                letter = point_str[0].upper()
                if not letter in BOARD_LETTERS:
                    raise ValueError(f"Invalid point_str: {point_str}")
                col = cls._col_letter_to_index(letter)
                row = int(point_str[1:])
            elif len(point_str) > 2 and '-' in point_str:
                col, row = map(int, point_str.split('-'))
            else:
                raise ValueError(f"Invalid point_str format: '{point_str}'")
            
            if not 1 <= col <= 19 or not 1 <= row <= 19:
                raise ValueError(f"Coordinates out of range: '{point_str}'")

            return cls(col, row)

        except (ValueError, IndexError):
            raise ValueError(f"Invalid point_str: '{point_str}'")

    @classmethod
    def parse(cls, point) -> 'Point':
        if isinstance(point, str):
            return cls.from_str(point)
        # elif isinstance(point, tuple):
        #     return cls.from_tup(point)
        # elif isinstance(point, dict):
        #     return cls.from_dict(cls, point)
        else:
            raise TypeError(f"Expected str, got {type(point)}")

    def __str__(self) -> str:
        """
        Returns a string representation of the point in 'A1' format.

        Returns:
            String representation of the point in the human-readable format "A1", "B3", etc.
        """
        s = ""
        col_letter = cls._col_letter_to_index(self[0])
        s += f"{col_letter}{20-self[1]}"
        return s

    def __eq__(self, value):
        return super().__eq__(value)


# +-------------------------+
# |   CUSTOM BOARD ERRORS   |
# +-------------------------+

class StonePlacementError(ValueError):
    """Raise when attempting to place a stone in a Board class where a stone already exists."""


# +-----------------+
# |   BOARD CLASS   |
# +-----------------+

class Board:
    """Represents the board of the game of Go."""
    def __init__(self, size: int = 19):
        """Initializes a new Board object

        Args:
            size (int, optional): Indicates the size of the game Board.
            Defaults to 19.
        """
        if size > 19 or size < 2:
            raise ValueError(f"Invalid board size: {size}")

        self.size = size
        # Storing the state as a list of lists with items set to either
        # Stone or None - aka Optional[Stone] aka Union[Stone, None].
        self.state: list[list[Optional[Stone]]] = [
            [None for _ in range(size)] for _ in range(size)
        ]
        # print(self.state)  # Uncomment to see the board representation on initialization.

    def __getitem__(self, point: Point) -> Optional[Stone]:
        if not isinstance(point, Point):
            raise TypeError(f"Expected a Point object, got {type(point)}")
        col, row = point
        return self.state[row-1][col-1]

    def __setitem__(self, point: Point, stone: Optional[Stone]):
        col, row = point
        self.state[row-1][col-1] = stone

    def __str__(self):
        s = ""
        letter_padding = len(BOARD_LETTERS[:self.size]) + (2*3)
        print(letter_padding)
        s += f"{BOARD_LETTERS[:self.size]:^{letter_padding}}\n"  # letters label
        for i, row in enumerate(reversed(self.state)):
            s += f"{(self.size - i):<3}"  # numbers label
            for stone in row:
                if stone == Stone.BLACK:
                    s += "X"
                elif stone == Stone.WHITE:
                    s += "O"
                else:
                    s += "."
            s += f"{(self.size - i):>3}\n"  # numbers label
        s += f"{BOARD_LETTERS[:self.size]:^{letter_padding}}\n"  # letters label
        s += "\n"
        return s

    def __eq__(self, other):
        if not isinstance(other, Board):
            return False
        if self.size != other.size:
            return False
        for point in self:
            if self[point] != other[point]:
                return False
        return True

    def __len__(self):
        return self.size

    def __iter__(self):
        """
        Returns an iterator over the board's points.
        """
        class BoardIterator:
            def __init__(self, board):
                self.board = board
                self.col, self.row = 1, 1
            
            def __next__(self):
                if self.row > self.board.size:
                    raise StopIteration
                point = Point(self.col, self.row)
                self.col += 1
                if self.col > self.board.size:
                    self.col = 1
                    self.row += 1
                return self.board[point]

        return BoardIterator(self)
