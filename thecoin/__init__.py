"""TheCoin.

The Coin hackaton game
"""

import configparser
from docopt import docopt
from thecoin.system import Game, World, Species, Being
from thecoin.rules import move_to


def main():
    """thecoin.

    The Coin hackaton game

    Usage: thecoin [options]

    Options:
      -h --help           Show this screen.
      --species=<config>  Species definition file
    """
    options = docopt(main.__doc__)
    species_config = configparser.ConfigParser()
    species_config.read(options['--species'])
    species = []
    for name, spcfg in species_config.items():
        if name == "DEFAULT":
            continue
        specie = Species(
            name=spcfg.get('name'),
            beings=[],
            factor_death_by_age=spcfg.getfloat('factor_death_by_age'),
            factor_reproductive_arity=spcfg.getfloat(
                'factor_reproductive_arity'),
            factor_tech_development=spcfg.getfloat('factor_tech_development'),
            avg_number_children=spcfg.getfloat('avg_number_children'))
        elements = spcfg.getint('initial_members')
        specie.beings = [
            Being(0, 0, 0, specie, False) for _ in range(elements)
        ]
        species.append(specie)

    initial_world = World(species, 0)
    game = Game(state=[initial_world])
