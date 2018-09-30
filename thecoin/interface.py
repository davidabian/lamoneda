"""Interface."""

from pathlib import Path
from contextlib import suppress
from dataclasses import dataclass
from typing import Sequence
import random
import glob

import cocos
import pygame
from cocos.text import Label
from cocos import scene
from cocos.layer import Layer
from cocos.director import director
from cocos.scenes import FadeTRTransition
from cocos.actions import JumpTo, MoveTo
from cocos.collision_model import CollisionManagerBruteForce
from cocos.sprite import Sprite
from cocos.audio.pygame.mixer import Sound

import pyglet
import pyglet.window.key

from thecoin.sprite import CollidableSprite
from thecoin.models import Being
from thecoin.rules import move_to

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


class TheCoinLayer(cocos.layer.ColorLayer, Layer):
    """The initial layer."""

    def __init__(self, game, interface, meta):
        self.meta = meta
        self.game = game
        pygame.mixer.init()
        pygame.mixer.music.load('audio/mariocoin.mp3')
        pygame.mixer.music.play()
        super().__init__(203, 207, 243, 255)
        toaster_sprite = Sprite('moneda.svg')
        toaster_sprite.scale = 0.5
        toaster_sprite.position = (director.get_window_size()[0] / 2,
                                   director.get_window_size()[1] / 2)
        self.add(toaster_sprite)
        self.has_ran = False
        self.schedule_interval(self.run, 4)

    def run(self, *args):
        if not self.has_ran:
            self.has_ran = True
            move_to(self.game, 0, 5)
            with suppress(Exception):
                director.replace(
                    FadeTRTransition(self.meta['scenes']['runner']))


class ToasterLayer(cocos.layer.ColorLayer, Layer):
    r"""Travel trough time


    ::

           __---~~~~--__                      __--~~~~---__
      `\---~~~~~~~~\\                    //~~~~~~~~---/'
        \/~~~~~~~~~\||                  ||/~~~~~~~~~\/
                    `\\                //'
                      `\\            //'
                        ||          ||
              ______--~~~~~~~~~~~~~~~~~~--______
         ___ // _-~                        ~-_ \\ ___
        `\__)\/~                              ~\/(__/'
         _--`-___                            ___-'--_
       /~     `\ ~~~~~~~~------------~~~~~~~~ /'     ~\
      /|        `\         ________         /'        |\
     | `\   ______`\_      \------/      _/'______   /' |
     |   `\_~-_____\ ~-________________-~ /_____-~_/'   |
     `.     ~-__________________________________-~     .'
      `.      [_______/------|~~|------\_______]      .'
       `\--___((____)(________\/________)(____))___--/'
        |>>>>>>||                            ||<<<<<<|
        `\<<<<</'                            `\>>>>>/'

    """

    def __init__(self, game, interface, meta):
        super().__init__(211, 214, 246, 255)
        self.game = game
        self.meta = meta
        self.interface = interface

        toaster_sprite = Sprite('toaster11.svg')
        toaster_sprite.scale = 0.5
        toaster_sprite.position = (director.get_window_size()[0] / 2,
                                   director.get_window_size()[1] / 2)
        self.add(toaster_sprite)
        self.label = Label(font_name="Helvetica", font_size=50)
        self.label.position = (toaster_sprite.position[0] - 110,
                               toaster_sprite.position[0] - 175)
        self.add(self.label)
        self.timer = 0
        self.schedule_interval(self.update_timer, 1)

    def update_timer(self, *args, **kwargs):
        """Update timer."""
        future = self.meta.get('direction_future')
        if self.meta['current_world'] == 0 and not future:
            with suppress(Exception):
                return director.replace(
                    FadeTRTransition(self.meta['scenes']['runner']))

        if future:
            self.timer += 1
        else:
            self.timer -= 1
            if self.timer <= 0:
                self.timer = 0

        if future and self.timer == self.meta["current_world"] + 5:
            self.meta['current_world'] = self.meta['current_world'] + 5
            self.meta['switch_world'] = True
            move_to(self.game, self.timer - 1, len(self.game.state) + 5)
            with suppress(Exception):
                return director.replace(
                    FadeTRTransition(self.meta['scenes']['runner']))

        if not future and self.timer == self.meta["current_world"] - 5:
            self.meta['current_world'] = self.meta['current_world'] - 5
            self.meta['switch_world'] = True
            move_to(self.game, self.timer, len(self.game.state) + 5)
            with suppress(Exception):
                return director.replace(
                    FadeTRTransition(self.meta['scenes']['runner']))

        self.label.element.text = "%s -> %s" % (self.meta["current_world"],
                                                self.timer)


class RunnerLayer(cocos.layer.ColorLayer, Layer):
    """State"""

    is_event_handler = True

    def __init__(self, game, interface, meta):
        super().__init__(242, 242, 242, 255)

        self.background = Sprite('fondo_final.svg', anchor=(0, 0))
        self.background.position = (0, 0)
        self.background.scale = 0.1
        self.add(self.background, z=0)
        self.has_ran = False
        self.schedule_interval(self.run, 4)

        self.game = game
        self.toaster = None
        self.toaster_back = None
        self.meta = meta

        self.meta["current_world"] = 0
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

    def switch_world(self):
        """Switch to a specific world."""
        self.current_screen = 0
        self.interface = Interface(
            5, self.game.state[self.meta['current_world']].characters,
            *director.get_window_size())
        self.do_draw()

    def do_draw(self):
        """Draw a screen."""
        self.main_character.x = 0
        self.main_character.y = 0
        self.main_character.do(
            MoveTo((self.interface.width, self.main_character.y), 10))

        for _, child in self.children:
            if child not in (self.main_character, self.background):
                self.remove(child)

        self.explosions = []
        self.collision_manager.clear()

        self.toaster = CollidableSprite("toaster00_future.svg")
        self.toaster.scale = 0.1
        self.toaster.position = (2 * random.randint(0, self.width) / 3 +
                                 self.width / 3), (random.randint(
                                     0, round(2 * self.height / 3)))
        self.add(self.toaster)
        self.collision_manager.add(self.toaster)

        if self.meta["current_world"] != 0:
            self.toaster_back = CollidableSprite("toaster00_past.svg")
            self.toaster_back.scale = 0.1
            self.toaster_back.position = (2 * random.randint(0, self.width) / 3
                                          + self.width / 3), (random.randint(
                                              0, round(2 * self.height / 3)))
            self.add(self.toaster_back)
            self.collision_manager.add(self.toaster_back)

        self.current_screen += 1
        for character in self.characters:
            self.sprites_by_id[id(character.sprite)] = character
            self.collision_manager.add(character.sprite)
            self.add(character.sprite)

        self.draw()

    def run(self, *args):
        if not self.has_ran:
            self.has_ran = True
            pygame.mixer.init()
            pygame.mixer.music.load('audio/Myvatn.mp3')
            pygame.mixer.music.play(-1)

    def check_finished(self, *args, **kwargs):
        """Check if has finished."""
        if self.meta.get('switch_world'):
            self.meta['switch_world'] = False
            self.switch_world()

        if self.main_character.x > self.interface.width:
            self.do_draw()

    def check_collisions(self, *args, **kwargs):
        """Check for collisions."""
        for elem in self.collision_manager.iter_colliding(self.main_character):
            if elem == self.toaster:
                position = self.toaster.position
                self.meta['direction_future'] = True
                self.remove(self.toaster)
                self.toaster = CollidableSprite("toaster01.svg")
                self.toaster.scale = 0.1
                self.toaster.position = position
                self.add(self.toaster)
                pygame.mixer.music.fadeout(1)
                with suppress(Exception):
                    director.replace(
                        FadeTRTransition(self.meta['scenes']['toaster']))

            if elem == self.toaster_back:
                position = self.toaster_back.position
                self.meta['direction_future'] = False
                self.remove(self.toaster_back)
                self.toaster_back = CollidableSprite("toaster10.svg")
                self.toaster_back.scale = 0.1
                self.toaster_back.position = position
                self.add(self.toaster_back)
                with suppress(Exception):
                    director.replace(
                        FadeTRTransition(self.meta['scenes']['toaster']))
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

    @property
    def world(self):
        """Get current world."""
        return self.game.state[self.meta["current_world"]]

    @property
    def characters(self):
        """Get current drawable characters"""
        return self.interface.screens[self.current_screen].characters
