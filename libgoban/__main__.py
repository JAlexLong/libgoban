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

"""Provides a minimalist cli interface to interactively use libgoban."""

from .board import *
from .game import *

from typing import Optional, Union

BANNER = """
▀██   ██  ▀██                      ▀██                       
 ██  ▄▄▄   ██ ▄▄▄    ▄▄▄ ▄   ▄▄▄    ██ ▄▄▄   ▄▄▄▄   ▄▄ ▄▄▄   
 ██   ██   ██▀  ██  ██ ██  ▄█  ▀█▄  ██▀  ██ ▀▀ ▄██   ██  ██  
 ██   ██   ██    █   █▀▀   ██   ██  ██    █ ▄█▀ ██   ██  ██  
▄██▄ ▄██▄  ▀█▄▄▄▀   ▀████▄  ▀█▄▄█▀  ▀█▄▄▄▀  ▀█▄▄▀█▀ ▄██▄ ██▄ 
                   ▄█▄▄▄▄▀                                  
"""

# +------------------------+
# |  GAME INITIALIZATION   |
# +------------------------+

def game_menu():
    print(BANNER)
    print("~~~ Welcome to the libgoban cli interface ~~~")
    # Select game mode
    while True:
        print()
        print("\nSelect game mode or enter 'q' to quit:")
        print("\t1) PvP")
        print("\t2) PvE")
        print("\t3) EvE")
        game_type= input(">>> ")
        if game_type == "1":
            pvp_game()
        elif game_type == "2":
            pve_game()
        elif game_type == "3":
            eve_game()
        elif game_type.lower() in ["q", "quit"]:
            break
        else:
            print(f"Invalid option: {game_type}")
            continue
        break

def create_player(player_num: int = 1, other_player: Optional[Union[Player, Engine]] = None) -> Player:
    """Retrieve necessary player info from stdin and return a Player object"""
    print(f"\n[+] Getting info for Player {player_num}.")
    name: str = get_player_name(player_num)
    if isinstance(other_player, type(None)):
        stone: Stone = get_player_stone(player_num)
    elif isinstance(other_player, Player):
        print(other_player, other_player.stone)
        stone: Stone = other_player.stone.OTHER
    else:
        raise InvalidPlayerError("Expected other_player to be of type Union[Player, Engine] but is of type {type(other_player)} instead.")
    # TODO: present info and confirm before submitting
    return Player(name, stone)

def get_player_name(player_num: int = 1) -> str:
    """Gets specified player name from stdin"""
    while True:
        print(f"\nWhat is your name, player {player_num}?")
        name = input(">>> ")
        if len(name) > 10:
            print("Name cannot be longer than 10 characters.")
            continue
        if not name.isalnum():
            print("Name must only contain alphanumeric characters.")
            continue
        return name

def get_player_stone(player_num: int = 1) -> Stone:
    """Gets which Stone the player prefers to play from stdin"""
    while True:
        print(f"\nWhich stones will you take, player {player_num}?")
        print("\t1) Black")
        print("\t2) White")
        stone_selection = input(">>> ")
        if stone_selection == "1":
            stone = Stone.BLACK
            break
        elif stone_selection == "2":
            stone = Stone.WHITE
            break
        else:
            print(f"Invalid option: {stone_selection}")
    return stone

def create_engine() -> Engine: ...

def create_game(player1: Union[Player, Engine], player2: Union[Player, Engine]) -> Game:
    """Retrieve necessary game info from stdin and return a Game object"""
    print("\n[+] Getting info for the game.")
    while True:
        print("\nWhat size board would you like to play on?")
        print("\t1) 9x9")
        print("\t2) 13x13")
        print("\t3) 19x19")
        game_size = input(">>> ")
        if game_size == "1":
            size = 9
            break
        elif game_size == "2":
            size = 13
            break
        elif game_size == "3":
            size = 19
            break
        else:
            print(f"Invalid option: {game_size}")
    return Game(player1, player2, Board(size))


# +------------------------+
# |     GAME INTERFACE     |
# +------------------------+

def player_turn(player: Player, game: Game): 
    if not player.stone == game.turn:
        raise TurnError()
    while True:
        # print board state
        print(BOARD_LETTERS[:game.board.size])
        print(game.board)
        print(BOARD_LETTERS[:game.board.size])
        # present options to player and get player input
        print("Enter your move or 'pass' to pass your turn.")
        point_input: str = input(">>> ")
        try:
            point = Point.parse(point_input)
        except:
            print("HEY WE NEED A VALID POINT PLZ")
            input()
            exit()
        move = Move(point, player.stone)
        # execute player command in game
        if move.islegal(game.board):
            game.make_move(move)
            break

def engine_turn(): ...

def pvp_game(): 
    # initialize players
    player1: Player = create_player()
    player2: Player = create_player(2, player1)
    # initialize game
    #game: Game = create_game(player1=player1, player2=player2)
    game = Game(player1, player2, Board(19))
    # game mainloop
    while True:
        if game.turn == player1.stone:
            player_turn(player1, game)
        elif game.turn == player2.stone:
            player_turn(player2, game)

def pve_game(): ...
def eve_game(): ...

def main():
    game_menu()

if __name__ == "__main__":
    main()
