"""Example script generating a message similar to `git -h` as seen in:
https://github.com/jazzband/docopt-ng/blob/master/examples/git/git.py

$ python examples/git/git_like.py

"""

from rich import print

from cli_help_maker import generator as gen


if __name__ == "__main__":
    generator = gen.HelpGenerator(
        prob_name_capitalized=0.,
        usage_section=False,
        options_section=False,
        options_header=False,
        argument_style="between_brackets",
        argument_documented_prob=0.0,
        option_documented_prob=0.0,
        description_before=False,
        program_description_prob=0.0,
        number_of_commands=0,
        number_of_options=10,
        options_shortcut=False,
        number_of_arguments=2,
        arguments_same_line=True
    )
    msg = generator.sample()
    # PARA CONSEGUIR TODOS LOS ARGUMENTOS EN LA MISMA LINEA (same_line) UTILIZAR
    # TEXTWRAP INDENT, CON INDENT INICIAL DIFERENTE, DE FORMA QUE QUEDE ALINEADO
    # -> PARA HACER EL EJEMPLO DE quick_example.py PARTIR DE UNA FUNCIÓN
    # QUE APILE LOS PROGRAMAS COMPLETOS.
    print(msg)
