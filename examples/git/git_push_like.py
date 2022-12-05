"""Example script generating a message similar to `git push -h` as seen in:
https://github.com/jazzband/docopt-ng/blob/master/examples/git/git_push.py

$ python examples/git_push_like.py

"""

from rich import print

from cli_help_maker import generator as gen


if __name__ == "__main__":
    generator = gen.HelpGenerator(
        indent_spaces=4,
        prob_name_capitalized=0,
        description_before=False,
        program_description_prob=0.0,
        usage_section=False,
        options_section=True,
        options_header=False,
        argument_style="between_brackets",
        argument_repeated=True,
        option_documented_prob=0.9,
        usage_pattern_capitalized=False,
        number_of_commands=1,
        number_of_options=16,
        option_argument_separator={
            "separator": False,
            "required": False,
        },
        options_shortcut=True,
        options_style={"style": "between_brackets"},
        number_of_arguments=1,
        arguments_same_line=True
    )
    msg = generator.sample()
    print(msg)