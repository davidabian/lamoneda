"""Interface."""
from dataclasses import dataclass
from typing import Sequence
import random
import string

from thecoin.system import Being


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
        screens = [
            Screen(i, self.width, self.height, [])
            for i in range(self.num_screens)
        ]
        for character in self.characters:
            if not character.touched:
                random.choice(screens).characters.append(character)
        return screens
