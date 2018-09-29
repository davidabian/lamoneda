"""Rules logic."""
import logging
import random
from pyknow import KnowledgeEngine
from pyknow import Fact
from pyknow import W
from pyknow import P
from pyknow import Rule
from pyknow import AND
from pyknow import OR
from pyknow import NOT
from pyknow import AS
from pyknow import CALL
from pyknow import watch
from pyknow import DefFacts
from pyknow.watchers import watch
from thecoin.system import Being
from thecoin.system import World

logging.basicConfig(level=logging.DEBUG)

watch("RULES", "FACTS", "AGENDA", "ACTIVATIONS")


class CharacterEvolution(KnowledgeEngine):
    """WorldFact evolution engine."""

    @DefFacts()
    def start(self, being):  # noqa
        """Define facts."""
        yield Fact(being=being)
        yield Fact(touched=being.touched)

    @Rule(
        AND(Fact(being=AS.being << W()),
            NOT(Fact(being=CALL.dead)),
            NOT(Fact(touched=True))))
    def is_not_dead(self, being):
        """Current character is not dead."""
        self.result.append(being)

    @Rule(AND(Fact(being=CALL.reproduces), Fact(being=AS.being << W())))
    def has_children(self, being):
        """Will have children."""
        children = random.randint(0, being.species.avg_number_children)
        self.result.extend([Being(0, being.species) for _ in range(children)])


def run(game, start_state, initial_species=False, expected_length=500):
    """Run KE."""

    if not game.state:
        game.state = [World(initial_species, 0)]
    # Remove future states, will be overwriten
    game.state = game.state[start_state:]
    while len(game.state) <= expected_length:
        world = game.state[-1]
        species = []
        for species in world.species:
            current_specie = []
            for being in species:
                ken = CharacterEvolution()
                ken.result = []
                ken.reset(being)
                ken.run()
                current_specie.extend(ken.result)
            species.append(current_specie)
        game.state.append(World(species, world.time + 1))
