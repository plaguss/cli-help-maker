"""_summary_
"""

import random

from .sampling import capitalize, make_word


def usage_pattern(capitalized: bool = True) -> str:
    usage = "usage: "
    if capitalized:
        return usage.capitalize()
    return usage


def section_pattern(section: str | None = "options", capitalized: bool = True) -> str:
    """Creates a section header.

    In general, the possible sections are `Arguments` or `Options`,
    but for example git has personalized headers on their sections.

    Args:
        section (str or None, optional): _description_. Defaults to 2.
        capitalized (float, optional): _description_. Defaults to 0.

    """
    if not section:
        section = make_word() + ":"
    else:
        section += ":"

    if capitalized:
        return section.capitalize()

    return section


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


def maybe_do_optional(content: str, probability: float = 0.5) -> str:
    """Calls `do_optional` with a probability given.

    Args:
        content (str): content as passed to `do_optional`
        probability (float, optional): _description_. Defaults to 0.5.

    Returns:
        str: _description_
    """
    if random.random() > (1 - probability):
        return do_optional(content)
    return content


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


def do_mutually_exclusive(content: list[str]) -> str:
    """Joins multiple options via pipes to create mutually exlusive
    elements.

    Args:
        content (list[str]): list of elements to join.

    Returns:
        str: _description_

    Note:
        Visit [docopt](https://github.com/jazzband/docopt-ng) pipe docs.
    """
    return " | ".join(content)


def do_mutually_exclusive_groups(
    elements: list[str],
    probability: float = 0.5,
    groups: list[int] = [0, 2],
    optional_probability: float = 0.5,
) -> list[str]:
    """Creates groups of mutually exclusive elements

    Args:
        elements (list[str]): Content for the groups, should be the list of options
            generated for a program.
        probability (float, optional): Probability of creating a group. Defaults to 0.5.
        groups (list[int], optional): Size of the groups. Defaults to [0, 2].
        optional_probability (float): probability of the group being optional.
            Otherwise it will be required.

    Returns:
        list[str]: _description_

    Note:
        The algorithm may benefit from some speed up, but
        is ok for the moment.
    """
    if len(elements) < 2:
        # The groups only have sense if there are 2 or more.
        return elements

    new_elements = []
    to_group = []
    group_size = random.choice(groups)
    for e in elements:
        to_group.append(e)
        if (
            len(to_group) == group_size
        ):  # Start with a simple option, later will use `groups`

            if random.random() > (1 - probability):
                to_group = do_mutually_exclusive(to_group)
                if random.random() > (1 - optional_probability):
                    to_group = do_optional(to_group)
                else:
                    to_group = do_required(to_group)
                new_elements.append(to_group)

            else:
                new_elements.extend(to_group)

            to_group = []
            # Restart the group size to allow taking a range of possibilities
            group_size = random.choice(groups)

    # Take care of the last options which didn't fit into a group
    # to avoid losing them
    if len(to_group) > 0:
        new_elements.extend(to_group)

    return new_elements


def options_shortcut(
    capitalized_probability: float = 0.0, all_caps: bool = False
) -> str:
    """Returns the shortcut for any options.

    Args:
        capitalized_probability (float, optional): Probability of returning
            the first capital letter. Defaults to 0.
        all_caps (bool, optional): If True, all the letters are in uppercase.
            For example, click uses this option. Defaults to False.

    Returns:
        str: [options] section.

    Note:
        https://github.com/jazzband/docopt-ng
    """
    options = capitalize("options", probability=capitalized_probability)
    shortcut = f"\[{options}]"
    if all_caps:
        return shortcut.upper()
    return shortcut
