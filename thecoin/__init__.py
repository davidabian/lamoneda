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
from cocos.actions import JumpTo, MoveTo
from cocos.collision_model import CollisionManagerBruteForce
from cocos.sprite import Sprite
import pyglet.window.key

from thecoin.system import Game, World, Species, Being
from thecoin.interface import Interface
from thecoin.rules import move_to
from thecoin.sprite import CollidableSprite

pyglet.resource.path.append(str((Path('.').parent / 'sprites').absolute()))
pyglet.resource.reindex()


class MainScene(Layer):
    """State"""

    is_event_handler = True

    def __init__(self, game, interface):
        super().__init__()
        self.game = game
        self.current_world = 0
        self.current_screen = 0
        self.space_used = 1
        self.interface = interface
        self.main_character = CollidableSprite('ppepotato.svg', anchor=(0, 0))
        self.collision_manager = CollisionManagerBruteForce()
        self.collision_manager.add(self.main_character)
        self.add(self.main_character)
        self.sprites_by_id = {}
        for character in self.characters:
            self.sprites_by_id[id(character.sprite)] = character
            self.collision_manager.add(character.sprite)
            self.add(character.sprite)

        self.main_character.do(
            MoveTo((self.interface.width, self.main_character.y), 10))

        self.schedule_interval(self.check_collisions, 0.1)

    def check_collisions(self, *args, **kwargs):
        """Check for collisions."""
        for elem in self.collision_manager.iter_colliding(self.main_character):
            self.sprites_by_id[id(elem)].touched = True
            explosion = Sprite('explosion.svg')
            explosion.position = elem.position
            try:
                self.remove(elem)
            except:
                pass
            self.add(explosion)

    def on_key_press(self, key, _):
        """Jumps."""
        if key == pyglet.window.key.SPACE:
            self.main_character.do(
                JumpTo((self.main_character.x + 50, 10), 100, 1, 0.8))

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
