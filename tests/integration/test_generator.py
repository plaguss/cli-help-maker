"""This file contains tests of the different functions used in cli_help_maker.generator.HelpGenerator.
"""


import random

import pytest

import cli_help_maker.generator as gen

FIXED_SEED = 6798


@pytest.fixture()
def help_generator_default():
    yield gen.HelpGenerator(
        indent_spaces=4,
        prob_name_capitalized=0,
        total_width=78,
        description_before=True,
        description_after=False,
        program_description_prob=0.5,
        usage_section=True,
        usage_pattern_capitalized=True,
        commands_section=False,
        commands_header=False,
        commands_capitalized=0,
        commands_documented_prob=0.01,
        arguments_section=False,
        arguments_header=False,
        arguments_style="between_brackets",
        argument_repeated=0.0,
        argument_documented_prob=0.9,
        arguments_pattern_capitalized=True,
        argument_capitalized_prob=0,
        argument_optional_prob=0.5,
        options_style={},
        options_section=False,
        options_header=False,
        option_documented_prob=0.9,
        options_pattern_capitalized=True,
        option_argument_separator=False,
        option_argument_required=False,
        options_mutually_exclusive_prob=0.0,
        options_mutually_exclusive_group=0,
        read_from_stdin=False,  # TODO: Not taken into account yet
        options_shortcut=1,
        options_shortcut_capitalized_prob=0.001,
        options_shortcut_all_caps=0,
        exclusive_group_optional_prob=0.5,
        number_of_commands=1,
        number_of_arguments=2,
        number_of_options=3,
        exclusive_programs=1,
    )


# Some basic tests just to ensure they are covered
def test_help_message(help_generator_default):
    assert help_generator_default.help_message == ""
    assert help_generator_default._current_length == 0
    help_generator_default.help_message = "some text"
    assert help_generator_default.help_message == "some text"
    assert help_generator_default._current_length == len("some text")


# Some basic tests just to ensure they are covered
def test_number_of_commands(help_generator_default):
    assert help_generator_default.number_of_commands == 1


def test_number_of_arguments(help_generator_default):
    assert help_generator_default.number_of_arguments == 2


def test_number_of_options(help_generator_default):
    assert help_generator_default.number_of_options == 3


@pytest.mark.parametrize(
    "help_gen, value, expected",
    [
        ("help_generator_default", 0, (0, 0)),
        ("help_generator_default", 1, (1, 1)),
        ("help_generator_default", 2, (2, 2)),
        ("help_generator_default", [0, 2], (0, 2)),
        ("help_generator_default", [1, 2], (1, 2)),
        ("help_generator_default", [3], (3, 3)),
        ("help_generator_default", "bad value", (3, 3)),
    ],
)
def test_check_number_of_elements(help_gen, value, expected, request):
    help_hen = request.getfixturevalue(help_gen)
    if isinstance(value, str):
        with pytest.raises(ValueError):
            help_hen._check_number_of_elements(value)

    else:
        opt = help_hen._check_number_of_elements(value)
        assert opt == expected


def test_description(help_generator_default):
    assert isinstance(help_generator_default._description(), str)


def test_program_name(help_generator_default):
    assert isinstance(help_generator_default._program_name(), str)


def test_commands(help_generator_default):
    cmds = help_generator_default._commands(total=-1)
    assert len(cmds) == 0
    assert len(help_generator_default._command_names) == 0
    cmds = help_generator_default._commands(total=0)
    assert len(cmds) == 0
    assert len(help_generator_default._command_names) == 0
    cmds = help_generator_default._commands(total=1)
    assert len(cmds) == 1
    cmds = help_generator_default._commands(total=9)
    assert len(cmds) == 9
    assert len(help_generator_default._command_names) == 10


@pytest.mark.parametrize(
    "help_gen, values, expected",
    [
        ("help_generator_default", ({}, False, False), "-P <untholeable>"),
        ("help_generator_default", ({}, False, True), "-P <untholeable>"),
        ("help_generator_default", ({}, True, True), "-d <tara-myxopoda>"),
        ("help_generator_default", ({}, True, True), "-d <tara-myxopoda>"),
    ],
)
def test_option(help_gen, values, expected, request):
    help_hen = request.getfixturevalue(help_gen)
    random.seed(FIXED_SEED)
    opt = help_hen._option(*values)
    assert opt == expected


@pytest.mark.parametrize(
    "help_gen, values, expected",
    [
        ("help_generator_default", (0, False, False), 0),
        ("help_generator_default", (1, False, False), 1),
        ("help_generator_default", (2, False, False), 2),
    ],
)
def test_options(help_gen, values, expected, request):
    help_hen = request.getfixturevalue(help_gen)
    opt = help_hen._options(*values)
    assert len(opt) == expected


@pytest.mark.parametrize(
    "help_gen, value, expected",
    [
        ("help_generator_default", 0, "[<areel-spaniellike>]"),
        ("help_generator_default", 1, "<areel-spaniellike>"),
    ],
)
def test_argument(help_gen, value, expected, request):
    help_hen = request.getfixturevalue(help_gen)
    random.seed(FIXED_SEED)
    arg = help_hen._argument(value)
    assert arg == expected


def test_argument_repeated(help_generator_default):
    assert len(help_generator_default._argument_names) == 0
    help_generator_default._argument_names.append("[<areel-spaniellike>]")
    assert help_generator_default._argument_names[0] == "[<areel-spaniellike>]"
    random.seed(FIXED_SEED)
    arg = help_generator_default._argument(0)
    assert arg == "[<areel-spaniellike>]"


@pytest.mark.parametrize(
    "help_gen, values, expected",
    [
        ("help_generator_default", (0, False), 0),
        ("help_generator_default", (1, False), 1),
        ("help_generator_default", (2, False), 2),
        ("help_generator_default", (2, True), 2),
    ],
)
def test_arguments(help_gen, values, expected, request):
    help_hen = request.getfixturevalue(help_gen)
    help_hen._argument_repeated = values[1]
    args = help_hen._arguments(total=values[0])
    if values[1] is True:
        assert args[-1].endswith("...")
    assert len(args) == expected
