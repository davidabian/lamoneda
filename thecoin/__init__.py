"""TheCoin.

The Coin hackaton game
"""

from docopt import docopt


def main():
    """thecoin.

    The Coin hackaton game

    Usage: thecoin [options]
    """
    options = docopt(main.__doc__)
    return options
