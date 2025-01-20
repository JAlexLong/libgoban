from dataclasses import dataclass
from enum import IntEnum
from typing import Optional


class PlayerType(IntEnum):
    PLAYER = 0
    CPU    = 1

@dataclass
class Player:
    name: str
    player_type: PlayerType
    stone: Optional[Stone]

@dataclass
class Move:
    point: Point
    stone: Stone

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



def main():
    player1 = Player("Black", PlayerType.PLAYER, Stone.BLACK)
    player2 = Player("White", PlayerType.CPU, Stone.WHITE)
    ruleset = RuleSet()
    game = Game(player1, player2, ruleset)
    print(game.board[0, 0])

if __name__ == '__main__':
    main()