TheCoin
-----------------------------

.. image:: https://travis-ci.org/XayOn/thecoin.svg?branch=master
    :target: https://travis-ci.org/XayOn/thecoin

.. image:: https://coveralls.io/repos/github/XayOn/thecoin/badge.svg?branch=master
 :target: https://coveralls.io/github/XayOn/thecoin?branch=master

.. image:: https://badge.fury.io/py/thecoin.svg
    :target: https://badge.fury.io/py/thecoin

The Coin hackaton game


Usage
-----

::

    thecoin.

    The Coin hackaton game

    Usage: thecoin [options]


Game mechanics
--------------

The game consist on a time-series status of a world, with only a limited set of variables describing it::
    Game = [
        TimeAndSpace(World(species=[Species1(reproduction_index=20, death_age=30, ...),
                                    Species2(reproduction_index=30, death_age=40, ...)]),
                           time=1),
        TimeAndSpace(World(species=[Species1(reproduction_index=20, death_age=30, ...),
                                    Species2(reproduction_index=30, death_age=40, ...)]),
                           time=2)]


At start, the user will see himself on a world with an initial state, raw, and
will have to avoid killing or interacting with any creatures. Any interaction
with any creature will trigger an action at the end of the level, wich will
potentially make big changes in the future.

At the end of the level, the user will be given a choice, WHEN to travel in its
toaster-based time machine, given it can travel to a max lenght in the future, and
to the first defined state in the past.

The creatures shown in the platform-like part of the game will be a
representation of the species statuses, i.e, if there are 3 million individuals
of one species, and one million individuals of another one, there could be 1
creature of the latest and 3 of the first.

This is represented that way because of the infinite-world nature of the game, as
it will keep going forever, each "screen" (as it rolls out to the next one)
will have a small representation of individuals, tough "touched" individuals
will be removed from any available screens, making it possible (way more
possible at the first of the game) to run out of creatures in the whole world.

The game is as simple as it gets, it scrolls at a stable speed, and you can
"flap" (like the famous flappy bird) by jumping in the air, with the space key.
It is an infinite map, as soon as you don't kill all the living things, in wich
case you'll be stuck on a dead, sad world.

As you "kill" native species such as mosquitoes, giant faces balls, and
amoebas, they'll be replaced by a cross.

You'll find TWO toasters, one of the will take you to 5 years into the future
and the other one 5 years into the past.

The game will predict the next five years using an expert system as soon as you
travel, having standard biological factors, such as species diversity,
reproductive capacity aging and death. Your changes in the past will heavily
affect how the ecosystem develops in the future.

This game:

- Has only one color
- Can be controlled with only one keystroke
- Represents the butterfly effect in biological ecosystems trough time
- It does not have any text (yet it does have a number)
- It is an infinite game
- It is a 2D game



Distributing
------------

Distribution may be done in the usual setuptools way.
If you don't want to use pipenv, just use requirements.txt file as usual and
remove Pipfile, setup.py will auto-detect Pipfile removal and won't try to
update requirements.

Note that, to enforce compatibility between PBR and Pipenv, this updates the
tools/pip-requires and tools/test-requires files each time you do a *dist*
command

General notes
--------------

This package uses PBR and pipenv.
Pipenv can be easily replaced by a virtualenv by keeping requirements.txt
instead of using pipenv flow.
If you don't need, or you're not actually using git + setuptools distribution
system, you can enable PBR manual versioning by creating a METADATA file with
content like::

    Name: thecoin
    Version: 0.0.1

Generating documentation
------------------------

This package contains a extra-requires section specifiying doc dependencies.
There's a special hook in place that will automatically install them whenever
we try to build its dependencies, thus enabling us to simply execute::

        pipenv run python setup.py build_sphinx

to install documentation dependencies and buildd HTML documentation in docs/build/


Passing tests
--------------

Running tests should always be done inside pipenv.
This package uses behave for TDD and pytest for unit tests, you can execute non-wip
tests and behavioral tests using::

        pipenv run python setup.py test


Docker
------

This package can be run with docker.

Default entry_point will be executed (thecoin) by default

This builds the docker for a SPECIFIC distributable release, that you need to
have previously built.

For this, do a release::

    python setup.py sdist

Grab the redistributable files::

    distrib=($(/bin/ls -t dist))

Now run docker build with it::

    docker build --build-arg distfile=${distrib[1]}


Attribution
------
Song used: https://archive.org/details/Retro_Masters-12650/Small_Colin_-_04_-_Myvatn.mp3 License: CC-BY-SA, Author: Small Colin
