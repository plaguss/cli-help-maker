"""Module in charge of generating CLI help messages. 

Currently only docopt is allowed.
"""

import random
import textwrap
from textwrap import indent

from .sampling import capitalize, make_argument, make_option, make_paragraph, make_word
from .utils import (
    do_mutually_exclusive_groups,
    do_optional,
    do_required,
    maybe_do_optional,
    options_shortcut,
    section_pattern,
    usage_pattern,
)

text_wrapper = textwrap.TextWrapper(width=78)


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
        - Change description_before to a tuple of position and probability
        - The option description is positioned starting at 2/3 the length
            decided for the console. The description must be adjusted
            if the arguments are longer.
        - Add arguments and options to a list, in case they are written inline
        and then documented on its section.
    """

    def __init__(
        self,
        indent_spaces: int = 2,
        prob_name_capitalized: float = 0,
        total_width: int = 78,
        description_before: bool = True,
        program_description_prob: float = 0.5,
        usage_section: bool = True,
        usage_first_line_aligned: bool = False,
        usage_pattern_capitalized: str = True,
        arguments_section: bool = False,
        arguments_header: bool = False,
        argument_style: str = "between_brackets",
        argument_repeated: bool = False,  # TODO: Make it a probability
        arguments_in_section: bool = False,
        argument_documented_prob: float = 0.9,
        arguments_pattern_capitalized: str = True,
        arguments_same_line: bool = True,  # What is this used for?
        options_style: dict = {},
        options_section: bool = False,
        options_header: bool = False,
        options_documented: bool = False,
        option_documented_prob: float = 0.9,
        options_pattern_capitalized: str = True,
        option_argument_separator: dict[str, bool] = {
            "separator": False,
            "required": False,
        },  # TODO: Make it a probability to allow having it only defined in a program.
        options_mutually_exclusive: dict[str, float | int] = {
            "probability": 0.0,
            "group": 0,
        },
        read_from_stdin: bool = False,  # TODO: Not taken into account yet
        options_shortcut: bool = False,
        number_of_commands: int | list[int] = 0,
        number_of_arguments: int | list[int] = 0,
        number_of_options: int | list[int] = 0,
        exclusive_programs: int = 1,
    ) -> None:
        """_summary_

        Args:
            indent_spaces (int, optional): _description_. Defaults to 2.
            prob_name_capitalized (float, optional): _description_. Defaults to 0.
            total_width (int): Total width allowed for the message. Defaults to 80
            description_before (bool): Whether to add description for the program
                before or after the program name.
            program_description_prob (float) TODO
            usage_section (bool) Determines the layout for the programs.
                It True, the programs are generated as a section, similar
                to optiosn and arguments. Defaults to True.
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
            option_documented_prob (float): Probability of documenting each
                option. Defaults to 0.9.
            options_mutually_exclusive (dict[str, float | int])
                Dict containing info with the probabilities of arguments being
                grouped. `probability` defines the probability of the elements
                being grouped, and `group` refers to the possible elements being
                grouped. The possible values are checked just like for number_of_...
                arguments. Wheter the grouped elements are optional or not, will
                be determined via the probability of the elements being optional.
                A list with a range of [0, 2] means at most 2 elements could
                be grouped.
            options_style (dict). Used to pass determined options' arguments instead
                of taking them randomly.
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
        self._total_width = total_width
        self._prob_name_capitalized = prob_name_capitalized
        self._options_style = options_style
        self._indent_spaces = indent_spaces
        self._usage_section = usage_section  # Used to split the programs in a section
        # or in the same line with indentation.
        self._usage_first_line_aligned = usage_first_line_aligned
        self._usage_pattern_capitalized = usage_pattern_capitalized
        self._arguments_section = arguments_section
        self._arguments_header = arguments_header
        self._argument_style = argument_style
        self._argument_repeated = argument_repeated
        self._argument_documented_prob = argument_documented_prob
        self._arguments_in_section = arguments_in_section
        self._arguments_pattern_capitalized = arguments_pattern_capitalized
        self._arguments_same_line = arguments_same_line
        self._options_section = options_section
        self._options_header = options_header
        self._options_documented = options_documented
        self._option_documented_prob = option_documented_prob
        self._option_argument_separator = option_argument_separator
        self._options_shortcut = options_shortcut
        self._options_pattern_capitalized = options_pattern_capitalized
        self._options_mutually_exclusive = {
            "probability": options_mutually_exclusive["probability"],
            "group": self._check_number_of_elements(
                options_mutually_exclusive["group"]
            ),
        }
        # Program description probability
        self._description_before = description_before
        self._program_description_prob = program_description_prob
        self._read_from_stdin = read_from_stdin
        self._exclusive_programs = exclusive_programs

        # Explain this is to allow working with a number of
        # exclusive_programs > 1
        self.number_of_commands = number_of_commands
        self.number_of_arguments = number_of_arguments
        self.number_of_options = number_of_options

        # Variables used to control the proper positioning
        # of the docs
        self._max_level_docs = int(1 / 3 * self._total_width)
        self._remaining_space_option_docs = int(
            self._total_width - self._max_level_docs
        )
        self._docs_limited = False

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
        """Checks the inputs given on number of commands or options.

        This arguments are expected to be an int, a list with one or two ints.
        """
        if isinstance(number, int):
            l, h = number, number
        elif isinstance(number, list):
            if len(number) == 1:
                l, h = number, number
            else:
                l, h = number[0], number[1]
        else:
            raise ValueError(f"Must be an int or a list of 2 ints")
        return l, h

    def _description(self) -> str:
        desc = make_paragraph()
        return text_wrapper.fill(desc)

    def _program_name(self) -> str:
        """Returns a name for the app."""
        return capitalize(make_word(), probability=self._prob_name_capitalized)

    def _commands(self, total: int = 0) -> list[str]:
        """Returns commands for the app.

        The commands are generated once, and

        i.e. `git add`, `git commit`, ...

        TODO: If a single argument is chosen, it will be written in the same
        line as the Usage: , otherwise it is written in the next line, using the
        indentation level chosen.
        """
        commands = [self._program_name() for _ in range(total)]
        self._command_names.append(commands)
        return commands

    def _option(self, options_arguments: dict, in_section: bool) -> str:
        """Creates an option for the message.

        A small subset of the arguments is generated here, those are allowed
        to behave differently across the same program.

        Args:
            options_arguments TODO: _description_.

        Returns:
            str: _description_
        """
        # These are dependent of the point where they are generated:
        if in_section:
            kwargs = {
                "short": random.choice([True, False]),
                "long": random.choice([True, False]),
                "with_value": random.choice([True, False]),
            }

        else:
            short = random.choice([True, False])
            long = not short
            kwargs = {
                "short": short,
                "long": long,
                "with_value": random.choice([True, False]),
            }

        options_arguments.update(
            {
                "short_capitalized_prob": 0.1,
                "long_capitalized_prob": 0,
            },
            **kwargs,
        )
        option = make_option(**options_arguments)
        # TODO: Consider using only the long name if available.
        self._option_names.append(option)

        return option

    def _options(self, total: int = 0, in_section: bool = False) -> list[str]:
        """Adds options to the help message.

        If `options_header` is set on construction, these will
        be written in a separate section.

        The options' layout is generated here to impose all the options
        for a program adhere to the same style.

        Args:
            total (int, optional): Number of options to generate. Defaults to 0.
            in_section (bool, optional): Whether the options are generated
                for a section or not. The arguments for the
                generator are slightly different. Defaults to False.

        Returns:
            list[str]: _description_
        """
        # TODO: Need to check the options are not the same (the probability
        # of happening is high when an option uses a single letter, i.e.:
        # -a, --attn  Rielbieo ergeetl els. Ef isbetbd. Ec ktoy ldg ooei. Ee nton
        #             uch hdrai
        # -a, --alab  Ias roron tlce. Namdgt euct le. Sheg pwlnanhd mnesa eaelap
        #             tnarn. Beb ln trrrsu
        # The following arguments are the same in general
        kwargs = {
            "short_separator": random.choice(["=", " "]),
            "long_separator": random.choice(["=", " "]),
            "short_long_separator": random.choice([", ", " "]),
            "probability_name_cap": 0,
            "probability_value_cap": 0,
            "style": random.choice(["between_brackets", "all_caps"]),
        }
        # TODO: Maybe this has no real reason to be here
        kwargs.update(**self._options_style)

        options = [self._option(kwargs, in_section) for _ in range(total)]
        return options

    def _argument(self, optional_probability: float = 0.5) -> str:
        """Creates an argument for a program.

        Args:
            optional_probability (float, optional): probability of the argument
                being optional. Defaults to 0.5.

        Returns:
            str: argument name
        """
        arg = make_argument(capitalized_prob=0, style=self._argument_style)
        self._argument_names.append(arg)
        if random.random() > optional_probability:
            arg = do_optional(arg)

        return arg

    def _arguments(self, total: int = 0) -> list[str]:
        """Generates a list of arguments. The last one can be repeated

        Args:
            total (int, optional): _description_. Defaults to 0.

        Returns:
            list[str]: _description_
        """
        # TODO: Allow adding the probability
        args = [self._argument() for _ in range(total)]

        if self._argument_repeated:
            args[-1] = args[-1] + "..."

        return args

    def _maybe_add_description(self) -> str:
        if random.random() > (1 - self._program_description_prob):
            return self._description()
        return ""

    def _add_program(self, prog_name: str, options_in_section: bool = False) -> None:
        """Single line program generator.

        Uses the program name as this may be reused.

        TODO: Keep track of the elements for the labels
        Args:
            prog_name : str
            number : int. Number of program written.
                For the moment is a simple way of keeping track of the indentation.
        """
        program = prog_name

        cmds = self._commands(total=self.number_of_commands)

        for c in cmds:
            cmd = " " + c
            program += cmd

        # For the length of the indentation, the relevant part are the program
        # name and subcommands
        subsequent_indent = (
            len(program)
            + len(usage_pattern(capitalized=self._usage_pattern_capitalized))
            + 1
        )

        if self._options_shortcut:
            # TODO: The probability should be defined outside:
            program += " " + options_shortcut(capitalized_probability=0.001, all_caps=0)

        if self._option_argument_separator["separator"]:
            sep = "--"
            if self._option_argument_separator["required"]:
                sep = maybe_do_optional(sep, probability=0.5)

            program += " " + sep

        # 3) options
        if not self._options_shortcut:
            # With options shortcut, these get written directly in a section
            opts = self._options(
                total=self.number_of_options, in_section=options_in_section
            )
            # If there are elements to group, do it first, then keep going:
            opts = do_mutually_exclusive_groups(
                elements=opts,
                probability=self._options_mutually_exclusive["probability"],
                groups=self._options_mutually_exclusive["group"],
                optional_probability=0.5,  # TODO: Get it from argument
            )

            for o in opts:
                # Only add the option if contained anything.
                if len(o) > 0:
                    if not "|" in o:
                        # Check for the pipe operator to avoid possibly making
                        # the argument twice optional.
                        o = maybe_do_optional(o, probability=0.5)

                    opt = " " + o

                    program += opt

        # 4) arguments
        args = self._arguments(total=self.number_of_arguments)

        for a in args:
            arg = " " + a
            program += arg

        self.help_message += "\n".join(
            textwrap.wrap(
                program,
                width=self._total_width,
                initial_indent="",
                subsequent_indent=" " * subsequent_indent,
            )
        )

    def _add_programs(self, prog_name: str) -> None:
        usage = usage_pattern(capitalized=self._usage_pattern_capitalized)
        self.help_message += usage

        if self._usage_section:
            self.help_message += "\n"
            indent_level = self._indent_spaces
        else:
            indent_level = len(usage)

        # If there are no exlusive programs, dont't do anything.
        # It there is one, let the options generated to be different
        # (as if added in a section).
        # Otherwise, generate multiple programs as is.
        def add_prog(indent_level, prog_name, options_in_section):
            self.help_message += " " * indent_level
            self._add_program(prog_name, options_in_section=options_in_section)
            self.help_message += "\n"

        if self._exclusive_programs == 1:
            if self._usage_section:
                level = indent_level
            else:
                level = 0

            add_prog(level, prog_name, self._options_section)

        elif self._exclusive_programs > 1:
            for i in range(self._exclusive_programs):
                level = 0 if (i == 0 and not self._usage_section) else indent_level
                add_prog(level, prog_name, False)

    def _add_section(
        self,
        elements: list[str],
        has_header: bool,
        section_name: str,
        capitalized: bool,
        documented_prob: float,
    ) -> None:
        """add_options_section and add_arguments_section can be generalized in this function
        with proper arguments.

        Args:
            elements (list[str]) Contains the arguments or options to add.
            has_header (bool) Whether to insert a header or not.
            section_name (str) 'arguments' or 'options' by default. TBD, not prepared
                to add random named section.
            capitalized (bool) 'arguments' or 'options' by default. TBD, not prepared
                to add random named section.
            documented_prob (float) Probability of options or arguments being documented.
        """
        if len(elements) > 0:
            if has_header:
                self.help_message += section_pattern(
                    section_name, capitalized=capitalized
                )
                self.help_message += "\n"

            opt_lengths = [len(o) + self._indent_spaces + 2 for o in elements]
            longest_opt = max(opt_lengths)

            if any(l > self._max_level_docs for l in opt_lengths):
                self._docs_limited = True
                longest_opt = self._max_level_docs

            for o, length in zip(elements, opt_lengths):
                opt = indent(o, " " * self._indent_spaces)
                opt = self._add_documentation(
                    opt,
                    longest_opt,
                    length,
                    documented_prob,
                )

                self.help_message += opt + "\n"
            self._docs_limited = False

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
        if random.random() > (1 - probability) and len(element) > 0:
            next_line = False
            if length > longest_elem:
                next_line = True
                length = longest_elem

            if self._docs_limited and next_line:
                element += "\n"
                initial_indent = subsequent_indent = self._max_level_docs
            else:
                initial_indent = longest_elem - length + 2
                subsequent_indent = longest_elem

            wp = textwrap.TextWrapper(
                width=self._total_width - self._indent_spaces,
                initial_indent=" " * initial_indent,
                subsequent_indent=" " * subsequent_indent,
            )
            docs = make_paragraph()
            pieces = wp.wrap(docs)
            # TODO: Not controlled yet
            # To control the length of the first line,
            # otherwise, given the smaller initial indent, doesn't
            # know the total length and the content is displaced to the right.
            # The first line is splitted to allow TextWrapper to wrap it correctly.
            # if len(pieces[0]) > (self._total_width - self._max_level_option_docs):
            #     pieces_ = [pieces[0][:self._remaining_space_option_docs],  " " * subsequent_indent + pieces[0][self._remaining_space_option_docs:]]
            #     if len(pieces) > 1:
            #         pieces = pieces_ + pieces[1:]
            #     else:
            #         pieces = pieces_
            description = "\n".join(pieces)
            # description = wp.fill(docs)
            element += description
        return element

    def _add_program_description(self) -> None:
        """Add the program description (randomnly)"""
        desc = self._maybe_add_description()
        if len(desc) > 0:
            if self._description_before:
                msg = desc + "\n" * 2
            else:
                msg = "\n" + desc + "\n"

            self.help_message += msg

    def sample(self) -> str:
        """Generates a sample help message

        Returns:
            str: _description_
        """

        if self._description_before:
            self._add_program_description()

        prog_name = self._program_name()
        self._add_programs(prog_name)

        if not self._description_before:
            self._add_program_description()

        if self._arguments_section:
            self.help_message += "\n"
            # If the arguments were created when calling _add_programs,
            # get them from the list of names. The same applies to the options.
            if self._argument_names:
                arguments = self._argument_names
            else:
                arguments = self._arguments(total=self.number_of_arguments)
            self._add_section(
                elements=arguments,
                has_header=self._arguments_header,
                section_name="arguments",
                capitalized=self._arguments_pattern_capitalized,
                documented_prob=self._argument_documented_prob,
            )

        if self._options_section:
            self.help_message += "\n"
            if self._option_names:
                options = self._option_names
            else:
                options = self._options(total=self.number_of_options, in_section=True)
            self._add_section(
                elements=options,
                has_header=self._options_header,
                section_name="options",
                capitalized=self._options_pattern_capitalized,
                documented_prob=self._option_documented_prob,
            )

        return self.help_message

    def labels(self) -> str:
        """Returns the help message annotated with the content"""
        raise NotImplementedError
        return ("Help message", [(1, 3, "ARGUMENT")])
