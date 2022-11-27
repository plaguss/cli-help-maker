"""Module in charge of generating CLI help messages. 

Currently only docopt is allowed.
"""

import random
import textwrap
from functools import partial
from textwrap import indent

from .sampling import (
    argument_styles,
    capitalize,
    make_argument,
    make_description,
    make_name,
    make_option,
    make_paragraph,
    make_word,
    randomize,
)

text_wrapper = textwrap.TextWrapper(width=80)


def usage_pattern(capitalized: bool = True) -> str:
    usage = "usage: "
    if capitalized:
        return usage.capitalize()
    return usage


def options_pattern(capitalized: bool = True) -> str:
    options = "options:"
    if capitalized:
        return options.capitalize()
    return options


def do_optional(content: str) -> str:
    """From http://docopt.org/

    Elements (options, arguments, commands) enclosed with square brackets
    "[ ]" are marked to be optional.

    Args:
        content (str): _description_

    Returns:
        str: _description_
    """
    return f"[{content}]"


def do_required(content: str) -> str:
    """From http://docopt.org/

    All elements are required by default, if not included in brackets "[ ]".
    However, sometimes it is necessary to mark elements as required explicitly
    with parens "( )".

    Args:
        content (str): _description_

    Returns:
        str: _description_
    """
    return f"({content})"


class HelpGenerator:
    """Class in charge of generating a help message and
    keep track of the steps involved to obtain the labeled
    content.

    help_message
        Contains the str message that would be printed
        in the console.
    _annotations
        A list of tuples of 3 elements, start position,
        end position and the corresponding entity.

    If the option arguments_in_section is set to False,
    argument_documented_prob won't be used as they won't
    be documented.

    Multiple program lines after the usage pattern mean
    several exclusive patterns.
    When exclusive_programs is used, the number of commands, options
    and arguments would be used for each exclusive program.

    TODO:
        Change description_before to a tuple of position and probability
    """

    def __init__(
        self,
        indent_spaces: int = 2,
        prob_name_capitalized: float = 0,
        options_style: dict = {},
        usage_section: bool = True,
        arguments_section: bool = False,
        arguments_header: bool = False,
        options_section: bool = False,
        options_header: bool = False,
        usage_first_line_aligned: bool = False,
        argument_style: str = "between_brackets",
        argument_repeated: bool = False,
        arguments_in_section: bool = False,
        options_documented: bool = False,
        total_width: int = 78,
        argument_documented_prob: float = 0.1,
        option_documented_prob: float = 0.9,
        description_before: bool = True,
        # description: bool = False,
        usage_pattern_capitalized: str = True,
        options_pattern_capitalized: str = True,
        number_of_commands: int = 0,  # TODO: Change to use a range -> int | list[int] = 1 | [1, 3]
        number_of_arguments: int = 0,  # TODO: Change to use a range
        number_of_options: int = 0,  # TODO: Change to use a range
        read_from_stdin: bool = False,
        option_argument_separator: dict[str, bool] = {
            "separator": False,
            "required": False,
        },
        options_shortcut: bool = False,
        arguments_same_line: bool = True,
        exclusive_programs: int = 1,
    ) -> None:
        """_summary_

        Args:
            indent_spaces (int, optional): _description_. Defaults to 2.
            prob_name_capitalized (float, optional): _description_. Defaults to 0.
            options_style (dict, optional): _description_. Defaults to {}.
            options_header (bool, optional): _description_. Defaults to True.
            usage_first_line_aligned (bool, optional): _description_. Defaults to False.
            argument_repeated (bool, optional): If given, the last argument
                can have any number of arguments. Defaults to False.
            arguments_documented (bool, optional): Whether an argument
                is documented. CHANGE TO A PROBABILITY. Defaults to False
            arguments_in_section (bool, optional): If True, writes the arguments
                on its own section, otherwise they are written as single
                line programs. Defaults to False
            total_width (int): Total width allowed for the message. Defaults to 80
            option_documented_prob (float): Probability of documenting each
                option. Defaults to 0.9.
            description_before (bool): Whether to add description for the program
                before or after the program name.
            exclusive_programs (int): Number of exclusive programs, according
                to the usage pattern. When only one is given, a single program
                definition occurs. Used to differentiate between different subcommands
                or different meaning of the arguments. Defaults to 1.
        """
        self._help_message = ""
        self._current_length = 0
        self._annotations = []
        # To keep track of the options and arguments, in case
        # they are added as a single line and documented on
        # a different section.
        self._command_names = []
        self._option_names = []
        self._argument_names = []
        # Layout options
        self._prob_name_capitalized = prob_name_capitalized
        self._options_style = options_style
        self._indent_spaces = indent_spaces
        self._usage_section = usage_section  # Used to split the programs in a section
        # or in the same line with indentation.
        self._arguments_section = arguments_section
        self._arguments_header = arguments_header
        self._options_section = options_section
        self._options_header = options_header
        self._usage_first_line_aligned = usage_first_line_aligned
        self._argument_style = argument_style
        self._argument_repeated = argument_repeated
        self._argument_documented_prob = argument_documented_prob
        self._arguments_in_section = arguments_in_section
        self._options_documented = options_documented
        self._total_width = total_width
        self._option_documented_prob = option_documented_prob
        self._description_before = description_before
        self._usage_pattern_capitalized = usage_pattern_capitalized
        self._options_pattern_capitalized = options_pattern_capitalized
        self._read_from_stdin = read_from_stdin
        self._option_argument_separator = option_argument_separator
        self._options_shortcut = options_shortcut
        self._arguments_same_line = arguments_same_line
        self._exclusive_programs = exclusive_programs

        # Explain this is to allow working with a number of
        # exlusive_programs > 1
        self.number_of_commands = number_of_commands
        self.number_of_arguments = number_of_arguments
        self.number_of_options = number_of_options

    @property
    def help_message(self) -> str:
        """Anytime the message is updated, the current lenght
        is updated when the setter is called."""
        return self._help_message

    @help_message.setter
    def help_message(self, msg: str) -> str:
        self._help_message = msg
        self._current_length += len(msg)

    @property
    def number_of_commands(self) -> int:
        return self._number_of_commands()

    @number_of_commands.setter
    def number_of_commands(self, number: int | list[int]) -> None:
        l, h = self._check_number_of_elements(number)
        self._number_of_commands = lambda: random.randint(l, h)

    @property
    def number_of_arguments(self) -> int:
        return self._number_of_arguments()

    @number_of_arguments.setter
    def number_of_arguments(self, number: int | list[int]) -> None:
        l, h = self._check_number_of_elements(number)
        self._number_of_arguments = lambda: random.randint(l, h)

    @property
    def number_of_options(self) -> int:
        return self._number_of_options()

    @number_of_options.setter
    def number_of_options(self, number: int | list[int]) -> None:
        l, h = self._check_number_of_elements(number)
        self._number_of_options = lambda: random.randint(l, h)

    def _check_number_of_elements(self, number: int | list[int]) -> tuple[int, int]:
        if isinstance(number, int):
            l, h = number, number
        elif isinstance(number, list) and len(number) == 2:
            l, h = number[0], number[1]
        else:
            raise ValueError(f"Must be an int or a list of 2 ints")
        return l, h

    def description(self) -> str:
        desc = make_paragraph()
        return "\n".join(text_wrapper.wrap(desc))

    def program_name(self) -> str:
        """Returns a name for the app."""
        return capitalize(make_word(), probability=self._prob_name_capitalized)

    def commands(self, total: int = 0) -> list[str]:
        """Returns commands for the app.

        i.e. `git add`, `git commit`, ...

        TODO: If a single argument is chosen, it will be written in the same
        line as the Usage: , otherwise it is written in the next line, using the
        indentation level chosen.
        """
        commands = [self.program_name() for _ in range(total)]
        self._command_names = commands
        return commands

    def option(self) -> str:
        return make_option(**self._options_style)

    def options(self, total: int = 0) -> list[str]:
        """Adds options to the help message.

        If `options_header` is set on construction, these will
        be written in a separate section.

        Args:
            total (int, optional): _description_. Defaults to 0.

        Returns:
            list[str]: _description_
        """
        # TODO: Need to check the options are not the same (the probability
        # of happening is high when an option uses a single letter, i.e.:
        # -a, --attn  Rielbieo ergeetl els. Ef isbetbd. Ec ktoy ldg ooei. Ee nton
        #             uch hdrai
        # -a, --alab  Ias roron tlce. Namdgt euct le. Sheg pwlnanhd mnesa eaelap
        #             tnarn. Beb ln trrrsu
        options = [self.option() for _ in range(total)]
        self._option_names = options
        return options

    def argument(self, optional_probability: float = 0.5) -> str:
        """Creates an argument for a program.

        Args:
            optional_probability (float, optional): probability of the argument
                being optional. Defaults to 0.5.

        Returns:
            str: argument name
        """
        arg = make_argument(capitalized_prob=0, style=self._argument_style)
        if random.random() > optional_probability:
            arg = do_optional(arg)

        return arg

    def arguments(self, total: int = 0) -> list[str]:
        """Generates a list of arguments. The last one can be repeated

        Args:
            total (int, optional): _description_. Defaults to 0.

        Returns:
            list[str]: _description_
        """
        args = [self.argument() for _ in range(total)]
        # Store the argument names in case they are documented later.
        self._argument_names += args

        if self._argument_repeated:
            args[-1] = args[-1] + "..."

        return args

    def maybe_add_description(self) -> str:
        if random.random() > 0.5:
            return self.description() + "\n"
        return ""

    def add_program(self, prog_name: str) -> None:
        """Single line program generator.

        Uses the program name as this may be reused.

        TODO: Keep track of the elements for the labels
        Args:
            prog_name : str
            number : int. Number of program written.
                For the moment is a simple way of keeping track of the indentation.
        """
        # TODO: 
        # Control if textwrap.wrap should be used as in comments,
        # may need a new argument from add_programs.
        # 1) program name
        program = prog_name
        self.help_message += prog_name

        # 2) command (more than one)
        cmds = self.commands()

        for c in cmds:
            cmd = " " + c
            program += cmd
            self.help_message += cmd

        if self._options_shortcut:
            self.help_message += " \[options]"

        if self._option_argument_separator["separator"]:
            sep = "--"
            if self._option_argument_separator["required"]:
                sep = do_optional(sep)

            self.help_message += " " + sep

        # 3) options
        opts = self.options()

        for o in opts:
            opt = " " + o
            program += opt
            self.help_message += opt

        # 4) arguments
        args = self.arguments(total=self.number_of_arguments)

        for a in args:
            arg = " " + a
            program += arg
            self.help_message += arg

    def add_programs(self, prog_name: str) -> None:
        usage = usage_pattern(capitalized=self._usage_pattern_capitalized)
        self.help_message += usage

        if self._usage_section:
            self.help_message += "\n"
            indent_level = self._indent_spaces
        else:
            indent_level = 0

        for _ in range(self._exclusive_programs):
            self.help_message += " " * indent_level
            self.add_program(prog_name)
            self.help_message += "\n"

    def add_arguments_section(self) -> None:
        # FIXME, DOESN'T WORK
        arguments = self.arguments(total=self._number_of_arguments)
        # FIXME: The arguments only are documented if they are written
        # in a separate section
        if len(arguments) != 0:
            arg_lengths = [len(a) for a in arguments]
            longest_arg = max(arg_lengths)

            for a, length in zip(arguments, arg_lengths):
                if self._arguments_in_section:
                    self._add_documentation(
                        a, longest_arg, length, self._argument_documented_prob
                    )

                self.help_message += " " + a + "\n"

    def add_options_section(self) -> None:
        # TODO: Rewrite everything related to options here.
        options = self.options(total=self.number_of_options)

        if len(options) > 0:
            if self._options_header:
                self.help_message += options_pattern(
                    capitalized=self._options_pattern_capitalized
                )
                self.help_message += "\n"

        # When adding the options, check the max length of them and add
        # the longest word in chars plus two if a description is given.
        opt_lengths = [len(o) for o in options]
        longest_opt = max(opt_lengths)

        # TODO: Escribir como método
        for o, length in zip(options, opt_lengths):
            # Version withoud docstrings
            # self.help_message += indent(opt, " " * self._indent_spaces) + "\n"
            opt = indent(o, " " * self._indent_spaces)
            opt = self._add_documentation(
                opt, longest_opt, length, self._option_documented_prob
            )

            self.help_message += opt + "\n"

    def _add_documentation(
        self, element: str, longest_elem: int, length: int, probability: float
    ) -> str:
        """Adds documentation to an alement.

        Can be used in arguments or options.

        Args:
            element (str): An argument or an option.
            longest_elem (int): The number of characters of the longest element.
            length (int): The number of characters of the current element.

        Returns:
            str: _description_
        """
        if random.random() > (1 - probability):
            indent_level = longest_elem - length + 2
            subsequent_indent_length = longest_elem + 2 + self._indent_spaces

            wp = textwrap.TextWrapper(
                width=self._total_width - subsequent_indent_length,
                initial_indent=" " * indent_level,
                subsequent_indent=" " * subsequent_indent_length,
            )
            docs = make_paragraph()
            description = "\n".join(wp.wrap(docs))
            element += description
        return element

    def sample(self) -> str:
        """Generates a sample help message

        Returns:
            str: _description_
        """

        if self._description_before:
            # Write this to a function
            self.help_message += self.maybe_add_description() + "\n"

        prog_name = self.program_name()
        self.add_programs(prog_name)
        # self.help_message += usage_pattern(capitalized=self._usage_pattern_capitalized)
        # self.help_message += prog_name

        if not self._description_before:
            # Write this to a function
            self.help_message += self.maybe_add_description()

        # The prior lines should be replace with the following:
        # self.add_program(prog_name, subcommands=[""], options=[""], arguments=[""])

        # for c in self.commands(total=self.number_of_commands):
        #     self.help_message += " " + c

        # if self._options_shortcut:
        #     self.help_message += " \[options]"

        # if self._option_argument_separator["separator"]:
        #     sep = "--"
        #     if self._option_argument_separator["required"]:
        #         sep = do_optional(sep)

        #     self.help_message += " " + sep

        # TODO: Review the arguments and options sections,
        # the names must be gathered from the variables 
        # _argument_names it they already appeared.

        if self._arguments_section:
            self.help_message += "\n" * 2
            self.add_arguments_section()

        if self._options_section:
            self.help_message += "\n" * 2
            self.add_options_section()

        return self.help_message

    def labels(self) -> str:
        """Returns the help message annotated with the content"""
        raise NotImplementedError
        return ("Help message", [(1, 3, "ARGUMENT")])


def options_shortcut(capitalized_probability: float = 0.0) -> str:
    """Returns the shortcut for any options.

    Args:
        capitalized_probability (float, optional): _description_. Defaults to 0.01.

    Returns:
        str: [options] or [OPTIONS] with `capitalized_probability`.

    Note:
        https://github.com/jazzband/docopt-ng
    """
    options = capitalize("options", probability=capitalized_probability)
    return f"\[{options}]"
