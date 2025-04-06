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

from .game import *

from rich import print
from typing import Union

BANNER = """
▀██   ██  ▀██                      ▀██                       
 ██  ▄▄▄   ██ ▄▄▄    ▄▄▄ ▄   ▄▄▄    ██ ▄▄▄   ▄▄▄▄   ▄▄ ▄▄▄   
 ██   ██   ██▀  ██  ██ ██  ▄█  ▀█▄  ██▀  ██ ▀▀ ▄██   ██  ██  
 ██   ██   ██    █   █▀▀   ██   ██  ██    █ ▄█▀ ██   ██  ██  
▄██▄ ▄██▄  ▀█▄▄▄▀   ▀████▄  ▀█▄▄█▀  ▀█▄▄▄▀  ▀█▄▄▀█▀ ▄██▄ ██▄ 
                   ▄█▄▄▄▄▀                                  
"""

# GAME INITIALIZATION

def get_player_info(player_num: int = 1) -> Player:
    """Retrieve necessary player info from stdin and returns a Player object"""

    print(f"\n[bold][+] Getting info for Player {player_num}.[/]")
    
    # get player.name
    while True:
        print(f"\nWhat is your name, player {player_num}?")
        name = input(">>> ")
        if len(name_selection) > 10:
            print("Name cannot be longer than 10 characters.")
            continue
        if not name_selection.isalnum():
            print("Name must only contain alphanumeric characters.")
            continue
        break

    # get player.stone
    while True:
        print("\nWhich stones will you take, [bold]player {player_num}[/]?")
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
            print(f"[bold red]Invalid option:[/] {stone_selection}")
    
    return Player(name, stone)

def get_engine_info() -> Engine: ...

def get_game_info(player1: Union[Player, Engine], player2: Union[Player, Engine]) -> Game:
    """Retrieve necessary game info from stdin and returns a Game object"""
    print("\n[bold][+] Getting info for the game.[/]")

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
            print(f"[bold red]Invalid option:[/] {game_size}")
    
    return Game(player1, player2, Board(size))


def start_pvp_game(): 
    # initialize players
    player1: Player = get_player_info()
    player2: Player = get_player_info(2)

    # initialize game
    game: Game = get_game_info(player1, player2)

    # mainloop
    while True:
        if game.turn == Stone.BLACK:
            player_turn()
        elif game.turn == Stone.WHITE:
            player_turn(2)

def start_pve_game(): ...
def start_eve_game(): ...

# GAME ROUTINES

def player_turn(): 
    # print board state
    # present options to player and get player input
    # execute player command in game
    pass

def engine_turn(): ...

def main():
    print(BANNER)
    print("~~~ Welcome to the libgoban cli interface ~~~")
    
    while True:
        print()
        print("\nSelect game mode or enter 'q' to quit:")
        print("\t1) PvP")
        print("\t2) PvE")
        print("\t3) EvE")
        game_type= input(">>> ")
        if game_type == "1":
            start_pvp_game()
            break
        elif game_type == "2":
            start_pve_game()
            break
        elif game_type == "3":
            start_eve_game()
            break
        elif game_type.lower() == "q":
            break
        else:
            print(f"Invalid option: {game_type}")

if __name__ == "__main__":
    main()
