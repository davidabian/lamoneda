"""TheCoin.

The Coin hackaton game
"""

import configparser
import random

import pyglet
from cocos import scene
from cocos.director import director

from docopt import docopt

from thecoin.models import Game, World, Species, Being
from thecoin.interface import RunnerLayer
from thecoin.interface import ToasterLayer
from thecoin.interface import TheCoinLayer
from thecoin.interface import Interface
from thecoin.rules import move_to


def main():
    """thecoin.

    The Coin hackaton game

    Usage: thecoin [options]

    Options:
      -h --help           Show this screen.
      --species=<config>  Species definition file
    """
    director.init()
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
    interface = Interface(5, game.state[0].characters,
                          *director.get_window_size())
    meta = {}
    runner = RunnerLayer(game, interface, meta)
    toaster = ToasterLayer(game, interface, meta)
    initial = TheCoinLayer(game, interface, meta)

    meta['scenes'] = {
        'runner': scene.Scene(runner),
        'toaster': scene.Scene(toaster),
        'initial': scene.Scene(initial)
    }

    director.run(meta['scenes']['initial'])
