"""Example script as in:
https://github.com/jazzband/docopt-ng/blob/master/examples/odd_even_example.py

NOTE: needs to work with examples.



$ python examples/odd_even_example_like.py

"""

from rich import print

from cli_help_maker import generator as gen


if __name__ == "__main__":
    generator = gen.HelpGenerator(
        indent_spaces=2,
        description_before=False,
        program_description_prob=0.0,
        argument_style="all_caps",
        argument_repeated=True,  # TODO: Needs a probability
        options_section=True,
        options_header=True,
        option_documented_prob=0.0,
        options_style={"short": True, "long": True, "with_value": False},
        options_mutually_exclusive={"probability": 1, "group": 2},
        number_of_commands=1,
        number_of_options=1,
        number_of_arguments=1,
        exclusive_programs=1,
    )
    msg = generator.sample()
    print(msg)
