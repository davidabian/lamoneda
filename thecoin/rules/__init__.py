"""Rules logic."""
import logging
from pyknow import KnowledgeEngine, Fact, W, P, Rule, AND, AS, watch, DefFacts, DefFacts
from pyknow.watchers import watch
from thecoin.system import TimeAndSpace, World

logging.basicConfig(level=logging.DEBUG)

watch("RULES", "FACTS", "AGENDA", "ACTIVATIONS")


class WorldFact(Fact):
    """WorldFact fact."""


class PreviousWorldFact(Fact):
    """WorldFact fact."""


class Action(Fact):
    """Define an action."""


class WorldFactEvolution(KnowledgeEngine):
    """WorldFact evolution engine."""

    @DefFacts()
    def start(self, state, action):  # noqa
        """Define facts."""
        yield PreviousWorldFact(population=state.world.population)
        yield Fact(time=state.time)
        yield Action(name=action)

    @Rule(
        WorldFact(population=P(lambda p: p >= 10) & AS.population << W()),
        salience=3)
    def world_will_reproduce(self, population):
        """World will reproduce."""
        self.next_state = TimeAndSpace(
            World(population=population * 2), time=self.time + 1)
        print(f'Everyone will reproduce')

    @Rule(
        WorldFact(population=P(lambda p: p < 10) & AS.population << W()),
        salience=2)
    def world_wont_reproduce(self, population):
        """World will not reproduce, trim population."""
        self.next_state = TimeAndSpace(
            World(population=population / 2), time=self.time + 1)
        print(f'Half population will die')

    @Rule(
        Action(name="kill"),
        PreviousWorldFact(population=AS.population << W()),
        salience=1)
    def kill(self, population):
        """Kill 10 people."""
        print("KILL")
        self.declare(WorldFact(population=population - 10))


def run(game, start_state, initial_population, action, expected_length):
    """Run KE."""
    if not game.state:
        game.state = [TimeAndSpace(World(initial_population), 0)]
    # Remove future states, will be overwriten
    game.state = game.state[start_state:]
    while len(game.state) <= expected_length:
        ken = WorldFactEvolution()
        ken.time = len(game.state) + 1
        ken.reset(state=game.state[-1], action=action)
        ken.run()
        game.state.append(ken.next_state)
