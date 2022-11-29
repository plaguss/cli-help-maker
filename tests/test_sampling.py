"""Tests for cli_help_maker.sampling. """

import random
random.seed(4657)

import cli_help_maker.sampling as smpl


def test_capitalize():
    assert smpl.capitalize("word", probability=1) == "Word"
    assert smpl.capitalize("word", probability=0) == "word"

def test_make_name():
    words = smpl.make_name(num_words=1).split(" ")
    assert len(words)  == 1
    words = smpl.make_name(num_words=3).split(" ")
    assert len(words)  == 3

def test_make_option():
    opt = smpl.make_option()
    assert opt == '-z, --zni'
