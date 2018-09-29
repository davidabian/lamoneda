"""TheCoin.

The Coin hackaton game
"""

import configparser
import random
from docopt import docopt
import pyglet
from pathlib import Path

import cocos
from cocos.text import Label
from cocos import scene
from cocos.layer import Layer
from cocos.director import director
from cocos.sprite import CollidableSprite
from cocos.actions import JumpTo
import pyglet.window.key

from thecoin.system import Game, World, Species, Being
from thecoin.interface import Interface
from thecoin.rules import move_to

pyglet.resource.path.append(str((Path('.').parent / 'sprites').absolute()))
pyglet.resource.reindex()


class MainScene(cocos.layer.ColorLayer, Layer):
    """State"""

    is_event_handler = True

    def __init__(self, game, interface):
        super( MainScene, self ).__init__(211,214,246,255)

        background_sprite = Sprite('fondo_final.svg', anchor=(0, 0))
        background_sprite.position = (0,0)
        background_sprite.scale = 0.1
        self.add(background_sprite, z=0)

        self.game = game
        self.current_world = 0
        self.current_screen = 0
        self.space_used = 1
        self.interface = interface
        self.main_character = CollidableSprite('ppepotato.svg')
        self.add(self.main_character)

        for character in self.characters:
            self.add(character.sprite)

    def on_key_press(self, key, _):
        """Jumps."""
        if key == pyglet.window.key.SPACE:
            self.main_character.do(
                JumpTo((self.main_character.x + 100, 10), 100, 1, 0.1))

    @property
    def world(self):
        """Get current world."""
        return self.game.state[self.current_world]

    @property
    def characters(self):
        """Get current drawable characters"""
        return self.interface.screens[self.current_screen].characters


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
    move_to(game, 0, 1)
    director.init()
    interface = Interface(5, game.state[0].characters,
                          *director.get_window_size())
    director.run(scene.Scene(MainScene(game, interface)))
