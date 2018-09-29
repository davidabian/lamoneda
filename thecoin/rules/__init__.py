"""Rules logic."""
from pyknow import KnowledgeEngine, Fact


class World(Fact):
    """World fact."""


class WorldEvolution(KnowledgeEngine):
    """World evolution engine."""

    def defFacts(self, start_time, world):
        """Define facts."""
        yield Fact(World(population=world.population))
        yield Fact(time=start_time)
