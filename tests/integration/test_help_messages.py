"""Tests for full messages generated.
"""

import json
import pathlib
import sys

import pytest
from rich import print

from cli_help_maker import generator as gen
from cli_help_maker.utils import highlight_message

# The following is done to allow getting the code in examples
# importable
examples_path = pathlib.Path(__file__).parent.parent.parent

if str(examples_path) not in sys.path:
    sys.path.append(str(examples_path))


def test_quick_example_like():
    from examples.quick_example_like import generator as gen

    annotations = json.loads(gen.annotations)
    # print("MESSAGE -> ")
    # print(annotations["message"])
    # print("ANNOTATIONS -> \n", annotations["annotations"])
    highlight_message(annotations)
    assert annotations == 1


@pytest.mark.skip
def test_git_add_like():
    generator = gen.HelpGenerator(
        indent_spaces=2,
        program_description_prob=1,
        argument_style="between_brackets",
        argument_documented_prob=1.0,
        options_section=True,
        options_header=True,
        options_shortcut=True,
        option_documented_prob=1,
        options_style={"style": "all_caps", "short_long_separator": ", "},
        options_mutually_exclusive={"probability": 1 / 15, "group": 2},
        number_of_commands=0,
        number_of_options=6,
        number_of_arguments=1,
        exclusive_programs=1,
    )
    # msg = generator.sample()
    annotations = json.loads(generator.annotations)
    print("MESSAGE -> ", annotations["message"])
    print("ANNOTATIONS -> ", annotations["annotations"])
    assert annotations == 1
