"""Rules logic."""
from dataclasses import replace
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
from pyknow.utils import freeze
from pyknow.utils import frozendict
from thecoin.models import Being
from thecoin.models import Species
from thecoin.models import World

# logging.basicConfig(level=logging.DEBUG)
# watch("RULES", "FACTS", "AGENDA", "ACTIVATIONS")


@freeze.register(Being)
def freeze_being(being):
    """Freeze being."""
    dict_ = being.__dict__.copy()
    dict_.pop('species')
    return frozendict(dict_)


class CharacterEvolution(KnowledgeEngine):
    """WorldFact evolution engine."""

    @DefFacts()
    def start(self, being, number):  # noqa
        """Define facts."""
        yield Fact(being=being)
        yield Fact(number=number)
        yield Fact(touched=being.touched)

    @Rule(
        AND(Fact(number=AS.number << W()),
            NOT(Fact(being=CALL.dead)),
            NOT(Fact(touched=True))))
    def is_not_dead(self, number):
        """Current character is not dead."""
        being = self.beings[number]
        self.result.append(replace(being))

    @Rule(AND(Fact(being=CALL.reproduces), Fact(being=AS.being << W())))
    def has_children(self, being):
        """Will have children."""
        children = random.randint(0, being.species.avg_number_children)
        self.result.extend([Being(0, being.species) for _ in range(children)])


def move_to(game, when, expected_length=10):
    """Move to a specific position in time and recalculate the future."""
    game.state = game.state[when:]
    while len(game.state) < expected_length:
        world = game.state[-1]
        species = []
        for species_ in world.species:
            current_specie = replace(species_, beings=[])
            beings = dict(enumerate(species_.beings))
            for number, being in beings.items():
                ken = CharacterEvolution()
                ken.result = []
                ken.beings = beings
                ken.reset(number=number, being=being)
                ken.run()
                current_specie.beings.extend(ken.result)
            species.append(current_specie)
        print(species)
        game.state.append(World(species, world.time + 1))
