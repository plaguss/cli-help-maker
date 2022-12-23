"""Tests of generator functions.

Only tested here isolated functions, the full generation of help messages
is done under tests/integration.
"""

import random

import pytest

import cli_help_maker.generator as gen

FIXED_SEED = 6798


@pytest.mark.xfail()
def test_argument_example_like():

    generator = gen.HelpGenerator(
        indent_spaces=2,
        usage_section=True,
        usage_pattern_capitalized=True,
        program_description_prob=1.0,
        description_before=False,
        arguments_section=True,
        arguments_header=True,
        arguments_style="all_caps",
        options_section=True,
        options_header=True,
        number_of_commands=2,
        number_of_options=[1, 3],
        number_of_arguments=1,
        exclusive_programs=2,
    )
    random.seed(FIXED_SEED)
    msg = generator.sample()
    text = """Usage: 
  prototype disdainful deacetylate [MYXOPODA-MICROCELLULAR]
  prototype crossleted opulency [UNDOING]

Tgalp rwoa lrrfaecle feep ume. Nvoepati lsoiiear cyn ma pwerk. Icces os
neenke.

Arguments:
  MYXOPODA-MICROCELLULAR  Thi if er. Lburrl isaa ioppp rrenr. Tnu dfwevpeta sa favto.
  UNDOING                 Tngty viosinugcy ran cronoel dre. Nsoe.

Options:
  -j=<troglodytism-shrift>
                          Odn ggoedu anrss.
"""
    assert msg == text
