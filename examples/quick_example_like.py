"""Example script generating a message similar to:
https://github.com/jazzband/docopt-ng/blob/master/examples/quick_example.py

$ python examples/quick_example_like.py

usage: ybde hd [options] [--] <lh>

    -e, --eleen  Llhnirsue desepte rhpoddjw. Aa ep ssice tnnch uxignn clpe
                 tts eucafe enct
    -o, --oefl   Rnsrh sope noei eoan rerimd naok teoaie nrano. Ka r. Ern
                 etint p
    -n, --nnsge
    -o, --os     Yyocvi aae oaedeae aahdu roueeriiy dstltno og hr

"""

from rich import print

from cli_help_maker import generator as gen


if __name__ == "__main__":
    generator = gen.HelpGenerator(
        indent_spaces=2,
        usage_section=True,
        program_description_prob=0.,
        arguments_section=False,
        options_section=False,
        usage_pattern_capitalized=True,
        number_of_commands=2,
        number_of_options=5,
        number_of_arguments=3,
        argument_style="between_brackets",
        exclusive_programs=3
    )
    msg = generator.sample()
    # PARA CONSEGUIR TODOS LOS ARGUMENTOS EN LA MISMA LINEA (same_line) UTILIZAR
    # TEXTWRAP INDENT, CON INDENT INICIAL DIFERENTE, DE FORMA QUE QUEDE ALINEADO
    # -> PARA HACER EL EJEMPLO DE quick_example.py PARTIR DE UNA FUNCIÓN
    # QUE APILE LOS PROGRAMAS COMPLETOS.
    print(msg)
