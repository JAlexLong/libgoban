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

        # input validation
        if not point_str or len(point_str) not in [2, 3]:
            raise ValueError(f"Invalid coordinate format: {point_str}\n\
                               Expected format 'a1', 'q11', etc.")
        col_letter = point_str[0].upper()
        if col_letter not in BOARD_LETTERS:
            raise ValueError(f"Invalid column letter: {col_letter}")

        # convert from letter in str to int
        col = ord(col_letter) - ord('A') + 1
        # adjust offset to account for missing 'I' in BOARD_LETTERS
        if col_letter in BOARD_LETTERS[7:]:
            col -= 1

        # convert str to int
        try:
            row = 20 - int(point_str[1:])
        except ValueError:
            raise ValueError(f"Invalid row number: {point_str[1:]}")

        return cls(col, row)

    def __str__(self) -> str:
        """
        Returns a string representation of the point.

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
        self.size = size
        # create an empty 2d list to hold the state of our Board class
        self.state: list[list[Optional[Stone]]] = [
            [None for _ in range(self.size)] for _ in range(self.size)
        ]
        # print(self.state)  # Uncomment to see the board representation

    def __getitem__(self, point: Point) -> Optional[Stone]:
        x, y = point
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.state[x][y]
        else:
            raise IndexError("Index out of bounds")

    def __setitem__(self, point: Point, stone: Optional[Stone]):
        x, y = point
        if 0 <= x < self.size and 0 <= y < self.size:
            self.state[x][y] = stone
        else:
            raise IndexError("Index out of bounds")

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
