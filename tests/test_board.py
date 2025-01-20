import pytest
from libgoban import Stone, Point, Board

def test_empty_board():
    board = Board()
    empty = [[None for _ in range(19)] for _ in range(19)]
    assert board.state == empty

def test_setitem():
    board = Board()
    point = Point(1, 1)
    board[point] = Stone.BLACK

    other_board = [[None] * board.size for _ in range(board.size)]
    other_board[0][0] = Stone.BLACK

    assert board.state == other_board