"""Base system."""
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
import itertools
import random
from thecoin.sprite import CollidableSprite


@dataclass
class Species:
    """Set of living beings of the same species."""

    # name (ID) of the species
    name: str

    beings: Sequence

    @property
    def population(self):
        """Population."""
        return len(self.beings)

    # Float: Multiplier for death probability by aging (i.e, age * this) ==
    # probability of dying
    factor_death_by_age: float

    # Float: Inverse multiplier for reproduction probability (i.e, age * -this)
    # == probabily of reproducing
    factor_reproductive_arity: float

    # Float, just specify if this is a tech_based society
    factor_tech_development: float

    # Average number of children for each time it reproduces
    avg_number_children: int


@dataclass
class Being:
    """Being."""
    age: int
    pos_x: int
    pos_y: int
    species: Species
    touched: bool
    pos_x: float  # in [0,1]
    pos_y: float  # in [0,1]

    @property
    def sprite(self):
        """Return a pyglet sprite."""
        if not hasattr(self, '_sprite'):
            self._sprite = CollidableSprite(self.sprite_file)
            self._sprite.position = self.pos_x, self.pos_y
            self._sprite.scale = 0.5
        return self._sprite

    def dead(self):
        """Return true if the being is dead on next iteration."""
        return self.species.factor_death_by_age*100 > random.randint(1,101)

    def reproduces(self):
        """Return true if the being reproduces."""
        return self.species.factor_reproductive_arity*100 > random.randint(1,101)

    @property
    def sprite_file(self):
        """Return sprite name"""
        return self.species.name + '.svg'


@dataclass
class World:
    """Position in time and space (state)."""
    species: Sequence[Species]

    # [0,1000]
    time: int

    @property
    def characters(self):
        return itertools.chain(*[a.beings for a in self.species])


@dataclass
class Game:
    """TimeAndSpace list"""
    state: Sequence[World]
