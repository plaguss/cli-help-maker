"""The HelpGenerator class is hard to test as it is, and its more interesting
to test if the generated message has the expected format than the inner
methods themselves.
"""


import pytest

import cli_help_maker.generator as gen

FIXED_SEED = 6798


@pytest.mark.skip(reason="not defined yet")
def test_argument_example_like():

    generator = gen.HelpGenerator(
        indent_spaces=2,
        usage_section=True,
        usage_pattern_capitalized=True,
        program_description_prob=1.0,
        description_before=False,
        arguments_section=True,
        arguments_header=True,
        arguments_style="all_caps",
        options_section=True,
        options_header=True,
        number_of_commands=2,
        number_of_options=[1, 3],
        number_of_arguments=1,
        exclusive_programs=2,
    )
    # random.seed(FIXED_SEED)
    msg = generator.sample()
    from rich import print

    # print(msg)
    text = """Usage: 
  prototype disdainful deacetylate [MYXOPODA-MICROCELLULAR]
  prototype crossleted opulency [UNDOING]

Stereophotogrammetry superintendency phelloderm felicitously hypobole.
Expostulate emmett muckweed provolunteering gyrocompass coalification
slovenlike buttered. Macrochiran twitten forgains.

Arguments:
  MYXOPODA-MICROCELLULAR  Adamite mussulmanism. Betso periodogram mylodont sniperscope
                          pentaglottical lapidarist. Scatterbrained gaine.
  UNDOING                 Shafted scratch enzymolysis stigonomancy sandclub
                          aspersion. Anemia inguinolabial bismillah
                          cynophilic. Engagedness college troller.
                          Covenanter mahdian corylus magnetron hematomancy
                          blatta fustigation. Eurypharynx ureterouteral
                          electrocutione.

Options:
  -m, --mancipleship   Meatiness thecitis deambulation. Subduple cofunction. Dynamo
                       picturemaking octagonally paraffine unrefinemen.
  --citellus-headsman  Perfervid harry. Eulytite lacustrian chapman tepomporize planosome
                       deportment. Monopyrenous matti telautomatically
                       originant birthmark acanthodean unacknowledging
                       quadric. Glycosuria soul accreditmen.
  -e=UNRICH            Canoness immediatist merveileux. Conjugationally flyingly
                       parathetic interantennal slopseller. Unburnt skinnery
                       areasoner guacico photobacteriu.
"""
    assert msg == text
