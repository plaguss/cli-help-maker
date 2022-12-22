"""CLI module to create a dataset of help messages. """

import random
import textwrap
from itertools import accumulate
from pathlib import Path
from typing import Callable

import srsly
import typer
from pydantic import BaseModel
from rich.progress import track

from cli_help_maker.generator import HelpGenerator

try:
    from ruamel.yaml import YAML

except ModuleNotFoundError:
    # TODO: Extend this message for any library outside of the main
    # dependencies.
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


app = typer.Typer()


class ArgumentField(BaseModel):
    """Pydantic model representing any of the values for an argument.

    Example:
        {'dist': 'range', 'parameters': {'values': [2, 4]}}
    """

    dist: str
    parameters: dict[str, list[float] | int | list[int] | list[str]]


class DatasetConfig(BaseModel):
    """Pydantic model to validate the fields in the .yaml file used to create a dataset.

    The attributes defined are those expected in the dataset.yaml file,
    and the values inside each argument are checked via ArgumentField.
    """

    version: str
    size: int
    arguments: dict[str, ArgumentField]


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

    dataset_config = DatasetConfig(**config)

    conf = {
        "version": dataset_config.version,
        "size": dataset_config.size,
        "arguments": {},
    }
    for k, v in dataset_config.arguments.items():
        conf["arguments"][k] = get_distribution(v.dict())

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
        if "value" not in parameters.keys():
            raise ValueError(
                f"'constant' dist expects a key 'value', you have: {parameters.keys()}"
            )
        return lambda: parameters["value"]
    elif dist == "set":
        if "values" not in parameters.keys():
            raise ValueError(
                f"'range' dist expects a key 'values', you have: {parameters.keys()}"
            )
        return lambda: random.choice(parameters["values"])
    elif dist == "uniform-discrete":
        if "min" not in parameters.keys() or "max" not in parameters.keys():
            raise ValueError(
                f"'uniform-discrete' dist expects key 'min' and 'max', you have: {parameters.keys()}"
            )
        return lambda: random.randint(parameters["min"], parameters["max"])
    elif dist == "uniform-continuous":
        if "min" not in parameters.keys() or "max" not in parameters.keys():
            raise ValueError(
                f"'uniform-continuous' dist expects key 'min' and 'max', you have: {parameters.keys()}"
            )
        return (
            lambda: parameters["min"]
            + (parameters["max"] - parameters["min"]) * random.random()
        )
    elif dist == "custom":
        if "values" not in parameters.keys() or "p" not in parameters.keys():
            raise ValueError(
                f"'custom' dist expects key 'values' and 'p', you have: {parameters.keys()}"
            )
        return lambda: random.choices(
            population=parameters["values"],
            cum_weights=list(accumulate(parameters["p"])),
        )[0]
    else:
        raise ValueError(f"`dist` field not defined: {dist}")


@app.command()
def main(
    input_path: Path = typer.Argument(
        "", exists=True, dir_okay=False, help="Path pointing to the .yaml file."
    ),
    output_path: Path = typer.Argument(
        "",
        dir_okay=False,
        help="Filename of the output path, the file extension will be .jsonl.",
    ),
    # spacy_format: bool = typer.Option(
    #     False,
    #     "-s",
    #     "--spacy",
    #     help="Generate both a .jsonl and a .spacy files. Defaults to False",
    # ),
):
    """Function to generate a dataset of cli help messages from a .yaml file
    with the info.
    """
    if output_path.suffix != ".jsonl":
        raise ValueError(f"output_path must have a filename ending in .jsonl or .spacy")
    # TODO: Use as a guide to translate the .jsonl file to a .spacy
    # https://github.com/explosion/projects/blob/v3/tutorials/ner_drugs/scripts/preprocess.py
    # TODO: Start here a DocBin?

    conf = read_config(input_path)
    input_generator = conf["arguments"]

    def annotation_writer(conf, input_generator):
        for i in track(range(conf["size"])):  # Value extracted from conf
            yield HelpGenerator(
                **{
                    "indent_spaces": input_generator["indent_spaces"](),
                    "total_width": input_generator["total_width"](),
                    "prob_name_capitalized": input_generator["prob_name_capitalized"](),
                    "description_before": input_generator["description_before"](),
                    "program_description_prob": input_generator[
                        "program_description_prob"
                    ](),
                    "usage_section": input_generator["usage_section"](),
                    "usage_pattern_capitalized": input_generator[
                        "usage_pattern_capitalized"
                    ](),
                    "commands_section": input_generator["commands_section"](),
                    "commands_header": input_generator["commands_header"](),
                    "commands_capitalized": input_generator["commands_capitalized"](),
                    "commands_documented_prob": input_generator[
                        "commands_documented_prob"
                    ](),
                    "arguments_section": input_generator["arguments_section"](),
                    "arguments_header": input_generator["arguments_header"](),
                    "arguments_style": input_generator["arguments_style"](),
                    "argument_repeated": input_generator["argument_repeated"](),
                    "argument_documented_prob": input_generator[
                        "argument_documented_prob"
                    ](),
                    "arguments_pattern_capitalized": input_generator[
                        "arguments_pattern_capitalized"
                    ](),
                    "argument_capitalized_prob": input_generator[
                        "argument_capitalized_prob"
                    ](),
                    "argument_optional_prob": input_generator[
                        "argument_optional_prob"
                    ](),
                    "options_section": input_generator["options_section"](),
                    "options_header": input_generator["options_header"](),
                    "option_documented_prob": input_generator[
                        "option_documented_prob"
                    ](),
                    "options_pattern_capitalized": input_generator[
                        "options_pattern_capitalized"
                    ](),
                    "options_shortcut": input_generator["options_shortcut"](),
                    "options_shortcut_capitalized_prob": input_generator[
                        "options_shortcut_capitalized_prob"
                    ](),
                    "options_shortcut_all_caps": input_generator[
                        "options_shortcut_all_caps"
                    ](),
                    "exclusive_group_optional_prob": input_generator[
                        "exclusive_group_optional_prob"
                    ](),
                    "options_mutually_exclusive_prob": input_generator[
                        "options_mutually_exclusive_prob"
                    ](),
                    "number_of_commands": input_generator["number_of_commands"](),
                    "number_of_arguments": input_generator["number_of_arguments"](),
                    "number_of_options": input_generator["number_of_options"](),
                    "exclusive_programs": input_generator["exclusive_programs"](),
                }
            )

    srsly.write_jsonl(
        path=output_path,
        lines=(gen.annotations for gen in annotation_writer(conf, input_generator)),
    )


if __name__ == "__main__":
    app()
