"""Example script generating a message similar to:
https://github.com/jazzband/docopt-ng/blob/master/examples/options_example.py

$ python examples/options_example_like.py

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
    generator = gen.HelpGenerator()
    msg = generator.sample()
    # PARA CONSEGUIR TODOS LOS ARGUMENTOS EN LA MISMA LINEA (same_line) UTILIZAR
    # TEXTWRAP INDENT, CON INDENT INICIAL DIFERENTE, DE FORMA QUE QUEDE ALINEADO
    # -> PARA HACER EL EJEMPLO DE quick_example.py PARTIR DE UNA FUNCIÓN
    # QUE APILE LOS PROGRAMAS COMPLETOS.
    print(msg)
