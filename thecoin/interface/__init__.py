import string
import random

from typing import Sequence

from thecoin.system import Being
from builtins import int
from dataclasses import dataclass

class Screen:
    """..."""
    id: int
    width: int
    height: int
    characters: Sequence[Being]

    @property
    def decoration(self):
        return [random.choice(sprites) 
                for _ in range(random.randint(sprites_per_screen))]

@dataclasss
class Interface:
    """..."""
    num_screens: int
    characters: Sequence[Being]
    width: int
    height: int

    @property
    def screens(self):
        screens = [Screen(i, self.width, self.height, []) 
                   for i in range(self.num_screens)]
        for character in self.characters:
            if not character.touched:
                random.choice(screens).characters.append(character)
        return screens

"""
interface = Interface(5, world.characters, 1680, 700)
while True:
    for screen in interface.screens:
       ...
"""