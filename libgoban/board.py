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
from typing import Optional, Tuple


# The letter 'I' is typically excluded to avoid confusion with 'J'
BOARD_LETTERS = "ABCDEFGHJKLMNOPQRST"


class Stone(IntEnum):
    """Represents the colors of stones in the game of Go."""
    BLACK = 0
    WHITE = 1

    @property
    def OTHER(self) -> 'Stone':
        """Returns the opposite color of the current stone."""
        return Stone((Stone.WHITE.value, Stone.BLACK.value)[self.value])


class Point(Tuple[int, int]):
    """
    Represents a point on a Go board.
    Coordinates are in the format (col, row) and are 1-based indexed.
    Inherits from typing.Tuple for immutability and efficiency.
    """
    def __new__(cls, col: int, row: int) -> 'Point':
        """
        Creates a new Point instance in the traditional Japanese format where 1-1
            is in the upper-left corner. I've chosen this format as the default
            because it is the closest to what our Board class will resemble.
            For more information, see https://senseis.xmp.net/?Coordinates
        Args:
            col: Column coordinate (1-indexed).
            row: Row coordinate (1-indexed).
        Returns:
            A new Point instance.
        """
        return super().__new__(cls, (col, row))

    @classmethod
    def parse(cls, point_str: str) -> 'Point':
        """
        Returns a Point instance from a string representation.
        Args:
            point_str: String representation of the point in the 'A1' format, where
                        'A1' is in the lower-left corner of the board.
                       'A1' == (1, 19), 'Q11' == (16, 9), etc. 
                       For more information, see https://senseis.xmp.net/?Coordinates
        Returns:
            A new Point instance.
        Raises:
            ValueError: If point_str fails input validation checks.
        """
        # TODO: Add 1-1 format parsing routines
        if type(point_str) != str:
            raise TypeError(f"Cannot parse Point from {type(point_str)}\n\
                              Try converting to str type first.")

        if len(point_str) > 3 or len(point_str) < 2:
            raise ValueError(f"Invalid coordinate format: '{point_str}'\n\
                               Expected format 'a1', 'q11', etc.")
        col_letter = point_str[0].upper()

        if col_letter not in BOARD_LETTERS:
            raise ValueError(f"Invalid column letter: '{col_letter}'\n\
                               Valid column letters are '{BOARD_LETTERS}'")

        col = ord(col_letter) - ord('A') + 1
        # adjust offset to account for missing 'I' in BOARD_LETTERS
        if col_letter in BOARD_LETTERS[7:]:
            col -= 1

        # convert str to int
        try:
            row = 20 - int(point_str[1:])
            if row < 1 or row > 19:
                raise ValueError
        except ValueError:
            raise ValueError(f"Invalid row number: {point_str[1:]}")

        return cls(col, row)

    def __str__(self) -> str:
        """
        Returns a string representation of the point in 'A1' format.

        Returns:
            String representation of the point in the human-readable format "A1", "B3", etc.
        """
        # adjusts offset to account for missing 'I' in valid_col_letters
        col_letter = chr(ord('A') + self[0] - 1) if self[1] <= 8 else chr(ord('A') + self[1])
        return f"{col_letter}{20-self[1]}"

    def __eq__(self, value):
        return super().__eq__(value)


class Board:
    def __init__(self, size: int = 19):
        """Initializes a new Board object

        Args:
            size (int, optional): Indicates the size of the game Board.
            Defaults to 19.
        """
        if size > 19 or size < 2:
            raise ValueError(f"Invalid board size: {size}")

        self.size = size
        self.state: list[list[Optional[Stone]]] = [
            [None for _ in range(size)] for _ in range(size)
        ]
        # print(self.state)  # Uncomment to see the board representation

    def __getitem__(self, point: Point) -> Optional[Stone]:
        col, row = point
        y = row - 1  # convert 1-based indexing to 0-based
        x = col - 1
        return self.state[y][x]

    def __setitem__(self, point: Point, stone: Optional[Stone]):
        col, row = point
        y = row - 1  # convert 1-based indexing to 0-based
        x = col - 1
        self.state[y][x] = stone

    def __str__(self):
        s = ""
        for y in range(self.size):
            for x in range(self.size):
                s += self.state[x][y] if type(self.state[x][y]) == Stone else '.'
                if len(s) % (self.size + len("\n")) == self.size:
                    s += "\n"
        return s

    def __eq__(self, other):
        for x in range(len(self)):
            for y in range(len(self)):
                if self[x][y] != other[x][y]:
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
                self.x = 0
                self.y = 0

            def __next__(self):
                if self.x >= self.board.size:
                    raise StopIteration
                point = (self.x, self.y)
                self.y += 1
                if self.y >= self.board.size:
                    self.y = 0
                    self.x += 1
                return point

        return BoardIterator(self)

    def get_neighbors(self, point: Point) -> list[Optional[Stone]]:
        """returns list of stones in neighboring squares

        Args:
            point (Point): coordinate of point on the Board in question

        Returns:
            list: [left, right, up, down]
        """
        x, y = point
        left_stone = self[point] if x != 0 else None
        right_stone = self[point] if x != self.size else None
        up_stone = self[point] if y != 0 else None
        down_stone = self[point] if y != self.size else None

        neighbors = [left_stone, right_stone, up_stone, down_stone]
        return neighbors

# @dataclass
# class Group:
#     stone: Stone  # represents the Stone that all members will be
#     seed: Point
#     _board: Board

#     def _find_members(self):
#         """Uses recursion to find all ally stones
#         This thing is a bit of a monster in terms of nesting... I will hopefully clean this up later
#         """
#         # break the recursion if we've already gone over all coordinates
#         _seen: list[Point] = []
#         if self.members == _seen:
#             return
