"""TheCoin.

The Coin hackaton game
"""

import configparser
import random
from docopt import docopt
import pyglet
from thecoin.system import Game, World, Species, Being
from thecoin.interface import Interface
from thecoin.rules import move_to

FPS = 1.0 / 170

WINDOW = pyglet.window.Window(fullscreen=True)

MAIN_CHARACTER = pyglet.sprite.Sprite(
    pyglet.image.load('sprites/ppepotato.svg'), 0, 0)


class State:
    """State"""
    game = None
    current_world = 0
    current_screen = 0
    space_used = 1
    interface = None

    @staticmethod
    def world():
        """Get current world."""
        return State.game.state[State.current_world]

    @staticmethod
    def characters():
        """Get current drawable characters"""
        return State.interface.screens[State.current_screen].characters


def update_pos(_):
    """Update position, just advance main user."""
    MAIN_CHARACTER.x += 10


@WINDOW.event
def on_draw():
    """Run each draw."""
    WINDOW.clear()
    img_background = pyglet.image.load('sprites/fondo_final.svg')
    img_background.blit(x=0, y=0, width=WINDOW.width, height=WINDOW.height)

    MAIN_CHARACTER.y = 0
    if State.space_used:
        State.space_used = False
        MAIN_CHARACTER.y += 200

    MAIN_CHARACTER.draw()

    for character in State.characters():
        character.sprite.draw()
        if character.collisions(MAIN_CHARACTER.x, MAIN_CHARACTER.y):
            character.touched = True


@WINDOW.event
def on_key_press(symbol, _):
    """On key press."""
    State.space_used = symbol == pyglet.window.key.SPACE


@WINDOW.event
def on_symbol_release(symbol, _):
    """On key press."""
    State.space_used = symbol == pyglet.window.key.SPACE


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
    State.game = Game(state=[initial_world])
    move_to(State.game, 0, 1)
    State.interface = Interface(5,
                                State.world().characters, WINDOW.width,
                                WINDOW.height)

    pyglet.clock.schedule_interval(update_pos, FPS)
    pyglet.app.run()
