"""Example script as in:
https://github.com/jazzband/docopt-ng/blob/master/examples/more_magic_like.py

$ python examples/more_magic_like.py
Usage: fmraumyaere [options] [ANAM]...
       fmraumyaere [options] ETTVUIE-NTC...

Zinle s tap. Cntmrr iel. Daerd hoet shti tydi cal en sana. C ebiney igtteo.

Options:
  --lro=ARLNCITPBI  Rreee oo. Mv.

NOTE: Not ready
"""

from rich import print

from cli_help_maker import generator as gen
from cli_help_maker.utils import highlight_message

generator = gen.HelpGenerator(
    total_width=72,
    usage_section=False,
    program_description_prob=1.,
    description_before=False,
    argument_style="all_caps",
    argument_documented_prob=1,
    argument_repeated=True,  # TODO: Make it a probability
    arguments_in_section=True,
    options_section=True,
    options_header=True,
    options_shortcut=True,  # TODO: This should be defined as a probability between programs
    option_documented_prob=1.,
    options_style={"long": True, "style": "all_caps"},
    number_of_options=[1, 2],
    number_of_arguments=[1, 2],
    exclusive_programs=2
)


if __name__ == "__main__":
    import json
    annot = generator.annotations
    highlight_message(json.loads(annot))
