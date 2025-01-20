import pytest
from libgoban import Point, Board

def test_empty_board():
    board = Board()
    empty = [[None for _ in range(19)] for _ in range(19)]
    assert board.state == empty