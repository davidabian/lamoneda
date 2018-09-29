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
