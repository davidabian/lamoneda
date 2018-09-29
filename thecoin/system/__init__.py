"""Base system."""
from dataclasses import dataclass
from typing import Sequence
import random


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
    species: Species
    touched: bool
    pos_x: float  # in [0,1]
    pos_y: float  # in [0,1]
    
    def dead(self):
        """Return true if the being is dead on next iteration."""
        probability_by_age = self.age * self.species.factor_death_by_age
        return probability_by_age > 100

    def reproduces(self):
        """Return true if user can reproduce."""
        return True
    
    @property
    def sprite_name(self):
        return self.being.species.name
    

@dataclass
class World:
    """Position in time and space (state)."""
    species: Sequence[Species]

    # [0,1000]
    time: int


@dataclass
class Game:
    """TimeAndSpace list"""
    state: Sequence[World]
