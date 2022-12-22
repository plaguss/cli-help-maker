"""Tests for cli_help_maker.cli functionalities. """

import pathlib

import pytest

from cli_help_maker import main

dataset_path = pathlib.Path(__file__).resolve().parent.parent / "dataset.yaml"


def test_read_config():
    conf = main.read_config(dataset_path)
    assert isinstance(conf, dict)
    assert len(conf.keys()) == 3
    keys = set(["version", "size", "arguments"])
    assert all([k in keys for k in conf.keys()])
    assert len(conf["arguments"]) == 33
    assert [
        callable(f) and f.__name__ == "<lambda>" for f in conf["arguments"].values()
    ]


def test_get_distribution():
    constant_dist = {"dist": "constant", "parameters": {"value": 1}}
    assert main.get_distribution(constant_dist)() == 1
    range_dist = {"dist": "range", "parameters": {"values": [2, 4]}}
    assert isinstance(main.get_distribution(range_dist)(), int)
    custom_dist = {"dist": "custom", "parameters": {"p": [0.2, 0.8], "values": [0, 1]}}
    assert isinstance(main.get_distribution(custom_dist)(), int)
    uniform_continuous_dist = {
        "dist": "uniform-continuous",
        "parameters": {"min": 0, "max": 1},
    }
    assert isinstance(main.get_distribution(uniform_continuous_dist)(), float)
    uniform_discrete_dist = {
        "dist": "uniform-discrete",
        "parameters": {"min": 0, "max": 10},
    }
    assert isinstance(main.get_distribution(uniform_discrete_dist)(), int)

    with pytest.raises(ValueError):
        assert main.get_distribution({"dist": "con", "parameters": {"value": 1}})() == 1
    with pytest.raises(ValueError):
        assert (
            main.get_distribution({"dist": "constant", "parameters": {"other": 1}})()
            == 1
        )
