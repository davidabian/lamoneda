
from thecoin.system import *

sprite_amoeba = "amoeba.svg"
amoeba = Species(name="Amoeba", beings=[], factor_death_by_age=0.2, factor_reproductive_arity=0.2, factor_tech_development=0.4, avg_number_children=2.5)
amoeba.beings = [Being(
    age=4,
    species=amoeba,
    touched=False,
    sprite_name=sprite_amoeba,
    pos_x=0.3,
    pos_y=0.3
    ), Being(
    age=10,
    species=amoeba,
    touched=False,
    sprite_name=sprite_amoeba,
    pos_x=0.7,
    pos_y=0.3
    )]

world = World(time=0, species=[amoeba])

interface = Interface(5, world.characters, 1680, 700)
while True:
    for screen in interface.screens:
        # Aqui deberian pintar interface.characters
        # Y cuando interactuen con un character, que se ponga touched=True
        pass