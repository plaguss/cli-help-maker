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
)

text_wrapper = textwrap.TextWrapper(width=80)

# TODO: Rewrite the following functions as a single one,
# taking care of the space in usage.

# TODO: Create decorator to allow functions be applied randomly


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
    """

    def __init__(
        self,
        indent_spaces: int = 2,
        prob_name_capitalized: float = 0,
        options_style: dict = {},
        options_header: bool = True,
        usage_first_line_aligned: bool = False,
        argument_style: str = "between_brackets",
        argument_repeated: bool = False,
        arguments_in_section: bool = False,
        options_documented: bool = False,
        total_width: int = 78,
        argument_documented_prob: float = 0.1,
        option_documented_prob: float = 0.9,
        description_before: bool = True,
        description: bool = False,
        usage_pattern_capitalized: str = True,
        options_pattern_capitalized: str = True,
        number_of_commands: int = 0,
        number_of_arguments: int = 0,
        number_of_options: int = 0,
        read_from_stdin: bool = False,
        option_argument_separator: dict[str, bool] = {
            "separator": False,
            "required": False,
        },
        options_shortcut: bool = False,
        arguments_same_line: bool = True,
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
        """
        self._help_message = ""
        self._current_length = 0
        self._annotations = []
        self._prob_name_capitalized = prob_name_capitalized
        self._options_style = options_style
        self._indent_spaces = indent_spaces
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

        # new params from sample, remove comment
        self._description = description
        self._usage_pattern_capitalized = usage_pattern_capitalized
        self._options_pattern_capitalized = options_pattern_capitalized
        self._number_of_commands = number_of_commands
        self._number_of_arguments = number_of_arguments
        self._number_of_options = number_of_options
        self._read_from_stdin = read_from_stdin
        self._option_argument_separator = option_argument_separator
        self._options_shortcut = options_shortcut
        self._arguments_same_line = arguments_same_line

    @property
    def help_message(self) -> str:
        """Anytime the message is updated, the current lenght
        is updated when the setter is called."""
        return self._help_message

    @help_message.setter
    def help_message(self, msg: str) -> str:
        self._help_message = msg
        self._current_length += len(msg)

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
        return [
            capitalize(make_word(), probability=self._prob_name_capitalized)
            for _ in range(total)
        ]

    def arguments(self, total: int = 0) -> list[str]:
        """Generates a list of arguments.

        Args:
            total (int, optional): _description_. Defaults to 0.

        Returns:
            list[str]: _description_
        """
        args = [
            make_argument(capitalized_prob=0, style=self._argument_style)
            for _ in range(total)
        ]
        # Do the arguments optional randomly
        args = [do_optional(arg) if (random.random() > 0.5) else arg for arg in args]

        if self._argument_repeated:
            args[-1] = args[-1] + "..."

        return args

    def options(self, total: int = 0) -> list[str]:
        """Adds options to the help message.

        If `options_header` is set on construction, these will
        be written in a separate section.

        Args:
            total (int, optional): _description_. Defaults to 0.

        Returns:
            list[str]: _description_
        """
        return [make_option(**self._options_style) for _ in range(total)]

    def maybe_add_description(self) -> str:
        if random.random() > 0.5:
            return self.description() + "\n\n"
        return ""

    def labels(self) -> str:
        """Returns the help message annotated with the content"""
        raise NotImplementedError
        return ("Help message", [(1, 3, "ARGUMENT")])

    def add_arguments(self) -> None:

        arguments = self.arguments(total=self._number_of_arguments)
        # FIXME: The arguments only are documented if they are written
        # in a separate section

        # When the args are documented:
        # 1) they need its own section
        # TODO: Define section for arguments
        # 2) The longest argument must be found,
        if len(arguments) != 0:
            if self._arguments_same_line:
                for arg in arguments:
                    self.help_message += " " + arg
            else:  # Arguments on its own section

                arg_lengths = [len(a) for a in arguments]
                longest_arg = max(arg_lengths)

                for a, length in zip(arguments, arg_lengths):
                    # 3) and each argument
                    #   must have as much spaces as the difference in letters
                    #   to the longest arg plus 2.
                    if self._arguments_in_section:
                        self._add_documentation(
                            a, longest_arg, length, self._argument_documented_prob
                        )

                    self.help_message += " " + arg + "\n"

    def add_options(self) -> None:
        # TODO: Rewrite everything related to options here.
        options = self.options(total=self._number_of_options)

        if len(options) > 0:
            if self._options_header:
                self.help_message += options_pattern(
                    capitalized=self._options_pattern_capitalized
                )

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
        # TODO: Create @randomize func.
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

        Args:
            description (bool, optional): _description_. Defaults to False.
            usage_pattern_capitalized (str, optional): _description_. Defaults to True.
            options_pattern_capitalized (str, optional): _description_. Defaults to True.
            number_of_commands (int, optional): _description_. Defaults to 0.
            number_of_arguments (int, optional): _description_. Defaults to 0.
            number_of_options (int, optional): _description_. Defaults to 0.
            read_from_stdin (bool, optional): _description_. Defaults to False.
            option_argument_separator (bool, optional): _description_. Defaults to True.
            option_argument_separator_required (bool, optional): _description_. Defaults to True.
            options_shortcut (bool): Adds an [option] to a program to avoid
                listing all commands together. See docopt.orgs' [options]. Defaults to False.
            arguments_same_line (bool): Places the arguments one next to the other

        Returns:
            str: _description_
        """

        if self._description_before:
            # Write this to a function
            self.help_message += self.maybe_add_description()

        prog_name = self.program_name()
        self.help_message += usage_pattern(capitalized=self._usage_pattern_capitalized)
        self.help_message += prog_name

        for c in self.commands(total=self._number_of_commands):
            self.help_message += " " + c

        if self._options_shortcut:
            self.help_message += " \[options]"

        if self._option_argument_separator["separator"]:
            sep = "--"
            if self._option_argument_separator["required"]:
                sep = do_optional(sep)

            self.help_message += " " + sep

        self.add_arguments()

        # TODO: Add the space only if there is further content
        self.help_message += "\n" * 2

        self.add_options()

        return self.help_message
