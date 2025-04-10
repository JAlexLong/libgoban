# libgoban

A Python library for working with the game of Go.

## Install it from PyPI (Not Yet Implemented)

***NOTE: THIS IS NOT AVAILABLE ON THE PyPI REPOSITORIES YET*** 
```bash
pip install libgoban
```

## Usage

You can use libgoban as a way to design and test bots, with a dummy bot

```py
import libgoban

player1 = Player(name="John Doe", stone=Stone.BLACK)
player2 = engine.DummyBot(stone=Stone.WHITE)

game = Game(player1=player1, player2=player2, size=19)
game.play()
```

You can also call the libgoban cli interface as a Python module or directly from the command line. 

```bash
$ python -m libgoban

# OR

$ libgoban
```
