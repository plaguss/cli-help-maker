"""CLI module to create a dataset of help messages.

Raises:
    KeyError: _description_
    ValueError: _description_

Returns:
    _type_: _description_
"""

from itertools import accumulate
from pathlib import Path
from typing import Callable

import typer
import textwrap
import random
import srsly
from .generator import HelpGenerator

try:
    from ruamel.yaml import YAML

except ModuleNotFoundError:
    from warnings import warn

    warn(
        textwrap.dedent(
            """To create a dataset from a yaml config file,
        first you need to install ruaml.yaml, either installing
        all the dependencies:

        $ pip install cli-help-maker[all]

        or installing ruaml.yaml:

        $ pip install ruaml.yaml
        """
        )
    )


def read_config(config: Path) -> dict[str, str]:
    """Reads a configuration file with the parameters to create a dataset
    of help messages.

    Parses the values and sets the generator functions for each argument.

    TODO: Document each argument in dataset.yaml:
    For example, indent spaces has a dist parameter which defines the type
    of distribution that should be used to generate the data.
    allowed ones are `uniform` and `constant` for the moment.
    Each dist has arguments, that would depend on the distribution.
    dist:
      uniform
    arguments:
      min: 2
      max: 4

    Args:
        config (Path) Path to the yaml config file.

    Notes
        An example of this file can be seen [here](https://github.com/plaguss/cli-help-maker/dataset.yaml)
    """
    yaml = YAML(typ="safe")  # default, if not specfied, is 'rt' (round-trip)
    with open(config, "r") as f:
        config = yaml.load(f)

    arguments = config["arguments"]
    conf = {}
    for k, v in arguments.items():
        # TODO: Check for any argument not found
        try:
            conf[k] = get_distribution(v)
        except KeyError:
            raise KeyError(f"Argument ({f}) isn't informed, please provide the info.")
    return conf


def get_distribution(data: dict[str, str | dict[str, int]]) -> Callable:
    """Get the distribution of an argument

    Args:
        data (dict) : TODO: Explain the possibilities.
            Gets the info from the field in the yaml file.

    Raises:
        ValueError: _description_

    Returns:
        Callable: _description_
    """
    dist, parameters = data["dist"], data["parameters"]
    if dist == "constant":
        return lambda: parameters["value"]
    elif dist == "range":
        return lambda: random.choice(parameters["values"])
    elif dist == "uniform-discrete":
        return lambda: random.randint(parameters["min"], parameters["max"])
    elif dist == "uniform-continuous":
        return (
            lambda: parameters["min"]
            + (parameters["max"] - parameters["min"]) * random.random()
        )
    elif dist == "custom":
        return lambda: random.choices(
            population=parameters["values"],
            cum_weights=list(accumulate(parameters["p"])),
        )
    else:
        raise ValueError(f"`dist` field not defined: {dist}")


def create_help_message_annotations(inputs: dict[str, int | str | bool | float]) -> str:
    """Helper function to generate the annotations of a help message from 
    a dict containing the inputs for HelpGenerator.

    Args:
        inputs (dict[str, int  |  str  |  bool  |  float]): Dict containing
            as keys the parameters and as values the input.

    Returns:
        str: str encoded json with the help message and the labels with positions.
    """

    gen = HelpGenerator(
        indent_spaces=2,
        prob_name_capitalized= 0,
        total_width= 78,
        description_before= True,
        program_description_prob = 0.5,
        usage_section= True,
        usage_pattern_capitalized = True,
        commands_section = False,
        commands_header = False,
        commands_capitalized = 0,
        commands_documented_prob = 0.01,
        arguments_section = False,
        arguments_header = False,
        argument_style = "between_brackets",
        argument_repeated = 0.0,
        argument_documented_prob = 0.9,
        arguments_pattern_capitalized = True,
        argument_capitalized_prob = 0,
        argument_optional_prob = 0.5,
        options_section = False,
        options_header = False,
        option_documented_prob = 0.9,
        options_pattern_capitalized = True,
        option_argument_separator = False,
        option_argument_required = False,
        options_mutually_exclusive_prob = 0.0,
        options_mutually_exclusive_group = 0,
        # read_from_stdin = False,  # TODO: Not taken into account yet
        options_shortcut = 0,
        options_shortcut_capitalized_prob = 0.001,
        options_shortcut_all_caps = 0,
        exclusive_group_optional_prob = 0.5,
        number_of_commands = 0,
        number_of_arguments = 0,
        number_of_options = 0,
        exclusive_programs = 1,
    )
    return gen.annotations


def main(
    input_path: Path = typer.Argument(
        ..., exists=True, dir_okay=False, help="Path pointing to the .yaml file."
    ),
    output_path: Path = typer.Argument(
        ...,
        dir_okay=False,
        help="Filename of the output path, the file extension will be .json.",
    ),
    spacy_format: bool = typer.Option(
        False, "-s", "--spacy", help="Generate both a .jsonl and a .spacy files. Defaults to False"
    ),
):
    """Function to generate a dataset of cli help messages from a .yaml file
    with the info.
    """
    if output_path.suffix != ".jsonl":
        raise ValueError(f"output_path must have a filename ending in .jsonl or .spacy")
    # TODO: Use as a guide to translate the .jsonl file to a .spacy
    # https://github.com/explosion/projects/blob/v3/tutorials/ner_drugs/scripts/preprocess.py
    # TODO: Start here a DocBin?

    # TODO: .spacy file will be generated AFTER the .jsonl has been generated

    conf = read_config(input_path)

    for i in range(conf["size"]):  # Value extracted from conf
        annotations = create_help_message_annotations()
        srsly.write_jsonl(
            path=output_path, data=annotations, append=True, append_new_line=True
        )


if __name__ == "__main__":
    typer.run(main)
