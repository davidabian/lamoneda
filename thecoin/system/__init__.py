"""Base system."""
from dataclasses import dataclass


@dataclass
class World:
    """Base world"""
    population: int

@dataclass
class TimeAndSpace:
    """Position in time and space (state)."""
    world: World

    # [0,1000]
    time: int

    # [-100,100]
    temperature: float

@dataclass
class Game:
    """TimeAndSpace list"""
    state: list

@dataclass
class Species:
    """Set of living beings of the same species."""

    # name (ID) of the species
    name: str

    # number of individuals
    population: int

    # sprite for species' city
    #sprite_city: str

    # [0,1], apriori probability of dying in a given time
    factor_aging: float

    # [0,1], apriori probability of having a reproduction in a given time
    factor_reproductive_arity: float

    # [0,1]
    factor_tech_development: float

    # [1,n], avg number of children in each reprodution
    avg_number_children: int

    # [-100,100]
    ideal_temperature: float

    # [-100,100]
    temperature_adaptability: float

