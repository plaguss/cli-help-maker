"""Tests for the expected data from calling the command line programs. """

import tempfile
from typer.testing import CliRunner
import srsly

from rich import print
import pathlib

from cli_help_maker import main
from cli_help_maker import utils


root = pathlib.Path(__file__).resolve().parent.parent.parent
dataset_path = root / "dataset.yaml"


runner = CliRunner()

def test_main():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = pathlib.Path(tmpdir)
        input_path = root / "tests" / "data" / "dataset.yaml"
        output_path = root / "tests" / "data" / tmpdir
        result = runner.invoke(main.app, [str(input_path), str(output_path)])
        arguments = tmpdir / "arguments.jsonl"
        dataset = tmpdir / "dataset.jsonl"
        assert arguments.is_file()
        assert dataset.is_file()
        data = list(srsly.read_jsonl(arguments))
        assert len(data) == 100
        data = list(srsly.read_jsonl(dataset))

        # Every dataset generated should have annotations inside the message,
        # otherwise there are labels that were annotated but weren't written
        # to the final message
        for line in data:
            message, annotations = line["message"], line["annotations"]
            utils.highlight_message(line)
            assert len(message) > annotations[-1][-1], utils.highlight_message(line)
