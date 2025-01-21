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

import pytest
from libgoban import Stone, Point, Board

def test_board_new():
    board = Board()
    empty = [[None for _ in range(19)] for _ in range(19)]
    assert board.state == empty

def test_board_getsetitem():
    board = Board()
    point = Point(1, 1)
    board[point] = Stone.BLACK

    expected = [[None] * board.size for _ in range(board.size)]
    expected[0][0] = Stone.BLACK

    assert board.state == expected

def test_board_print():
    board = Board()
    point_a1 = Point.parse("a1")
    point_tengen = Point.parse("k10")
    point_t19 = Point.parse("t19")

    board[point_a1] = Stone.BLACK
    board[point_tengen] = Stone.BLACK
    board[point_t19] = Stone.WHITE

    expected = 'X..................\n...................\n...................\n...................\n...................\n...................\n...................\n...................\n...................\n.........X.........\n...................\n...................\n...................\n...................\n...................\n...................\n...................\n...................\n..................O\n'
    assert str(board) == expected
