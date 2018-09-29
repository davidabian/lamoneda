"""Base system."""
from dataclasses import dataclass


@dataclass
class World:
    """Base world"""
    population: int


@dataclass
class TimeAndSpace:
    """Position in time and space."""
    world: World
    time: int


@dataclass
class Game:
    """TimeAndSpace list"""
    state: list
