"""TheCoin.

The Coin hackaton game
"""

from docopt import docopt
from thecoin.system import Game
from thecoin.rules import run


def main():
    """thecoin.

    The Coin hackaton game

    Usage: thecoin [options]
    """
    options = docopt(main.__doc__)
    game = Game(state=[])
    run(game, 0, 100, 'kill', 500)
    print(game.state)
