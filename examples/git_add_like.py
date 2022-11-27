"""Example script generating a message similar to `git add` as seen in:
https://github.com/jazzband/docopt-ng/blob/master/examples/git/git_add.py

$ python examples/git_add_like.py
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
        indent_spaces=4,
        prob_name_capitalized=0,
        usage_section=False,
        options_section=True,
        options_header=False,
        argument_style="between_brackets",
        argument_documented_prob=0.1,
        option_documented_prob=0.9,
        description_before=False,
        usage_pattern_capitalized=False,
        number_of_commands=1,
        number_of_options=4,
        option_argument_separator={
            "separator": True,
            "required": True,
        },
        options_shortcut=True,
        number_of_arguments=1,
        arguments_same_line=True

    )
    msg = generator.sample(
    )
    # PARA CONSEGUIR TODOS LOS ARGUMENTOS EN LA MISMA LINEA (same_line) UTILIZAR
    # TEXTWRAP INDENT, CON INDENT INICIAL DIFERENTE, DE FORMA QUE QUEDE ALINEADO
    # -> PARA HACER EL EJEMPLO DE quick_example.py PARTIR DE UNA FUNCIÓN
    # QUE APILE LOS PROGRAMAS COMPLETOS.
    print(msg)
