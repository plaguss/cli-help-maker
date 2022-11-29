

from cli_help_maker import generator as gen

import cli_help_maker.sampling as smpl


def printer(text):
    return text

@smpl.randomize(probability=1.)
def do_optional_always(content):
    return gen.do_optional(content)


@smpl.randomize(probability=0.)
def do_optional_never(content):
    return gen.do_optional(content)


def test_do_optional_randomized():
    value = "argument"
    assert do_optional_always(value) == f"[{value}]"
    assert do_optional_never(value) == value
