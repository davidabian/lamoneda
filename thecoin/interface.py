"""Interface."""
from dataclasses import dataclass
from typing import Sequence
import random

from thecoin.models import Being


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
                    character.pos_x = 2*random.randint(0, self.width)/3 + self.width/3
                    character.pos_y = random.randint(0, round(2 * self.height / 3))
                    random.choice(self._screens).characters.append(character)
        return self._screens
