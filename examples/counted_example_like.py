"""Example script as in:
https://github.com/jazzband/docopt-ng/blob/master/examples/naval_fate.py

$ python examples/naval_fate_like.py

"""

from cli_help_maker import generator as gen
from cli_help_maker.utils import highlight_message

generator = gen.HelpGenerator(
    # prob_name_capitalized=0.,
    # indent_spaces=2,
    # usage_section=True,
    # options_section=True,
    # options_header=True,
    # options_shortcut=False,
    # argument_style="between_brackets",
    # argument_documented_prob=0.0,
    # argument_repeated=True,
    # option_documented_prob=1.,
    # description_before=False,
    # program_description_prob=0.0,
    # number_of_commands=[0, 2],
    # number_of_options=[0, 2],
    # number_of_arguments=[0, 3],
    # # arguments_same_line=True,
    # exclusive_programs=6
)

if __name__ == "__main__":
    import json

    annot = generator.annotations
    highlight_message(json.loads(annot))
