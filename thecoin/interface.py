"""Interface."""

from pathlib import Path
from contextlib import suppress
from dataclasses import dataclass
from typing import Sequence
import random
import glob

import cocos
from cocos.text import Label
from cocos import scene
from cocos.layer import Layer
from cocos.director import director
from cocos.actions import JumpTo, MoveTo
from cocos.collision_model import CollisionManagerBruteForce
from cocos.sprite import Sprite

import pyglet
import pyglet.window.key

from thecoin.sprite import CollidableSprite
from thecoin.models import Being

RESOURCES = str((Path('.').parent / 'sprites').absolute())
pyglet.resource.path.append(RESOURCES)
pyglet.resource.reindex()


@dataclass
class Screen:
    """Represents a screen"""
    id: int
    width: int
    height: int
    characters: Sequence[Being]

    @property
    def decoration(self):
        """Return a list of decorative entries."""
        sprites = ['sprite_one', 'sprite_two']
        sprites_per_screen = 5
        return [
            random.choice(sprites)
            for _ in range(random.randint(0, sprites_per_screen))
        ]


@dataclass
class Interface:
    """Represents the game interface"""
    num_screens: int
    characters: Sequence[Being]
    width: int
    height: int

    @property
    def screens(self):
        """Extract next screens::

            interface = Interface(5, world.characters, 1680, 700)
            while True:
                for screen in interface.screens:
        """
        # TODO: rename num_screens by num_characters_by_screen

        if not hasattr(self, '_screens'):
            characters_ = list(self.characters)
            total_characters = len(characters_)
            num_screens = round(total_characters / self.num_screens)
            self._screens = [
                Screen(i, self.width, self.height, [])
                for i in range(num_screens)
            ]
            for character in characters_:
                if not character.touched:
                    character.pos_x = 2 * random.randint(
                        0, self.width) / 3 + self.width / 3
                    character.pos_y = random.randint(
                        0, round(2 * self.height / 3))
                    random.choice(self._screens).characters.append(character)
        return self._screens


class ToasterLayer(cocos.layer.ColorLayer, Layer):
    def __init__(self, game, interface):
        super(ToasterLayer, self).__init__(211, 214, 246, 255)
        toaster_sprite = Sprite('toaster11.svg')
        toaster_sprite.position = (director.get_window_size()[0] / 2, director.get_window_size()[1] / 2,)
        toaster_sprite.draw()


class RunnerLayer(cocos.layer.ColorLayer, Layer):
    """State"""

    is_event_handler = True

    def __init__(self, game, interface):
        super(RunnerLayer, self).__init__(211, 214, 246, 255)

        background_sprite = Sprite('fondo_final.svg', anchor=(0, 0))
        background_sprite.position = (0, 0)
        background_sprite.scale = 0.1
        self.add(background_sprite, z=0)

        self.game = game
        self.toaster = None
        self.current_world = 0
        self.current_screen = 0
        self.space_used = 1
        self.interface = interface
        self.main_character = CollidableSprite('ppepotato.svg', anchor=(0, 0))
        self.collision_manager = CollisionManagerBruteForce()
        self.collision_manager.add(self.main_character)
        self.add(self.main_character)
        self.sprites_by_id = {}
        self.explosions = []

        self.do_draw()

        self.schedule_interval(self.check_collisions, 0.1)
        self.schedule_interval(self.check_finished, 0.1)

    def do_draw(self):
        """Draw a screen."""
        self.main_character.x = 0
        self.main_character.y = 0
        self.main_character.do(
            MoveTo((self.interface.width, self.main_character.y), 10))

        for character in self.characters:
            with suppress(Exception):
                self.remove(character.sprite)

        for explosion in self.explosions:
            with suppress(Exception):
                self.remove(explosion)

        self.explosions = []
        self.collision_manager.clear()
        if self.toaster:
            self.remove(self.toaster)
        self.toaster = CollidableSprite("toaster00.svg")
        self.toaster.scale = 0.1
        self.toaster.position = (2 * random.randint(0, self.width) / 3 +
                                 self.width / 3), (random.randint(
                                     0, round(2 * self.height / 3)))
        self.add(self.toaster)
        self.collision_manager.add(self.toaster)

        self.current_screen += 1
        for character in self.characters:
            self.sprites_by_id[id(character.sprite)] = character
            self.collision_manager.add(character.sprite)
            self.add(character.sprite)

        self.draw()

    def check_finished(self, *args, **kwargs):
        """Check if has finished."""
        if self.main_character.x > self.interface.width:
            self.do_draw()

    def check_collisions(self, *args, **kwargs):
        """Check for collisions."""
        for elem in self.collision_manager.iter_colliding(self.main_character):
            if elem == self.toaster:
                position = self.toaster.position
                self.remove(self.toaster)
                self.toaster = CollidableSprite("toaster01.svg")
                self.toaster.scale = 0.1
                self.toaster.position = position
                self.add(self.toaster)
                continue
            if not id(elem) in self.sprites_by_id:
                continue
            self.sprites_by_id[id(elem)].touched = True
            explosion = Sprite('explosion.svg')
            explosion.scale = 0.5
            explosion.position = elem.position
            self.explosions.append(explosion)

            with suppress(Exception):
                self.remove(elem)
            self.add(explosion)

    def on_key_press(self, key, _):
        """Jumps."""
        if key == pyglet.window.key.SPACE:
            self.main_character.do(
                JumpTo((self.main_character.x + 50, 10), 100, 1, 0.8))
        elif key == pyglet.window.key.A:
            director.run(scene.Scene(ToasterLayer(game, interface)))

    @property
    def world(self):
        """Get current world."""
        return self.game.state[self.current_world]

    @property
    def characters(self):
        """Get current drawable characters"""
        return self.interface.screens[self.current_screen].characters
