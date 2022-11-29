"""Module defining the distribution of the different components in the apps.

For example, the names of the apps are ranged between 2 and 10 letters,
and are "roughly" distributed according to X.

This are used to obtain the content that would fill help messages.

When possible, the sampling distributions should match a real sample
of the population, otherwise they would be random with "commonsense"
options if possible.

https://arxiv.org/pdf/1207.2334.pdf
"""

import random
import string
from functools import wraps
from itertools import accumulate
from typing import Any, Callable
from warnings import warn

from lorem_text import lorem

# Letter frequency, obtained from the following link with the "script":
# https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
# import requests
# from bs4 import BeautifulSoup
# req = requests.get(r"https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html")
# soup = BeautifulSoup(req.content, "html.parser")
# table = soup.find_all("table")[-1].find_all("tr")
# letters = []
# freqs = []
# for row in table:
#     cols = [c for c in row.find_all("td")]
#     letters.append(cols[0].text)
#     letters.append(cols[3].text)
#     freqs.append(float(cols[1].text.replace("%", "")))
#     freqs.append(float(cols[4].text.replace("%", "")))

cap_letters = [
    "E",
    "M",
    "A",
    "H",
    "R",
    "G",
    "I",
    "B",
    "O",
    "F",
    "T",
    "Y",
    "N",
    "W",
    "S",
    "K",
    "L",
    "V",
    "C",
    "X",
    "U",
    "Z",
    "D",
    "J",
    "P",
    "Q",
]
LETTERS = [l.lower() for l in cap_letters]
LETTER_FREQUENCIES = [
    11.1607,
    3.0129,
    8.4966,
    3.0034,
    7.5809,
    2.4705,
    7.5448,
    2.072,
    7.1635,
    1.8121,
    6.9509,
    1.7779,
    6.6544,
    1.2899,
    5.7351,
    1.1016,
    5.4893,
    1.0074,
    4.5388,
    0.2902,
    3.6308,
    0.2722,
    3.3844,
    0.1965,
    3.1671,
    0.1962,
]

# Idea for the word length from:
# https://math.wvu.edu/~hdiamond/Math222F17/Sigurd_et_al-2004-Studia_Linguistica.pdf
# Function for probability of a word of length x (in letters).
# -> f = lambda x: 11.74 * (x ** 3) * (0.4 ** x)
f = lambda x: 11.74 * (x**3) * (0.4**x)
_word_length_probs = list(accumulate([f(x) for x in range(1, 30)]))
# Adjust the values to be in the range [0, 1], and remove those which are over 100.
WORD_LENGTH_PROBABILITIES = [i for i in _word_length_probs if i < 100] + [100]

g = lambda x: 1.1 * x * 0.9**x
_sentence_length_probs = list(accumulate([f(x) for x in range(1, 80)]))
SENTENCE_LENGTH_PROBABILITIES = [i for i in _sentence_length_probs if i < 100] + [100]


argument_styles = {
    "between_brackets": lambda w: f"<{w}>",
    "all_caps": lambda w: w.upper(),
}


def capitalize(content: str, probability: float = 0.5) -> str:
    """Capitalizes a string string with a given probability."""
    if random.random() > 1 - probability:
        return content.capitalize()
    return content


def word_length() -> int:
    """Generates the number of letters in a word using a more
    appropriate probability distribution than uniform.

    Returns:
        int: number of letters in a word.
    """
    return random.choices(
        range(1, len(WORD_LENGTH_PROBABILITIES) + 1),
        cum_weights=WORD_LENGTH_PROBABILITIES,
    )[0]


def sentence_length() -> int:
    """Like word length but for sentences.

    Returns:
        int: number of words in a sentence.
    """
    return random.choices(
        range(1, len(SENTENCE_LENGTH_PROBABILITIES) + 1),
        cum_weights=SENTENCE_LENGTH_PROBABILITIES,
    )[0]


def paragraph_length() -> int:
    # The number of sentences per paragraph is totally made up.
    return random.choices(
        range(1, 7),
        weights=[10.0, 25.0, 30.0, 20.0, 10.0, 5.0],
    )[0]


def randomize(probability: float = 1) -> Any:
    """Function decorator to apply the function to the element with the
    probability given.
    """

    def maybe_apply(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            value = args[0]
            if random.random() > (1 - probability):
                value = func(*args, **kwargs)
            return value

        return wrapper

    return maybe_apply


def make_word() -> str:
    return "".join(random.choices(LETTERS, weights=LETTER_FREQUENCIES, k=word_length()))


def make_sentence():
    return capitalize(
        " ".join([make_word() for _ in range(sentence_length())]), probability=1
    )


def make_paragraph():
    return ". ".join([make_sentence() for _ in range(paragraph_length())])[:-1]


def name_length(min_letters: int = 2, max_letters: int = 10) -> int:
    """Returns the number of characters in a name.

    Corresponds to the program, i.e. `git`, `ls`.
    """
    num_letters = random.randint(min_letters, max_letters)
    return num_letters


def argument_length(min_letters: int = 2, max_letters: int = 10) -> int:
    """Currently a copy of the name sampler."""
    return name_length(min_letters=min_letters, max_letters=max_letters)


def make_description(min_num_words: int = 2, max_num_words: int = 30) -> str:
    """Returns a possible description for a program or argument.
    Currently the number of words is a uniform variable in the range
    [min_num_words, max_num_words], set by default to 2 and 30 respectively.
    """
    num_words = random.randint(min_num_words, max_num_words)
    return lorem.words(num_words)


def make_composed_word() -> str:
    """Generator of composed words for arguments, with
    made-up probabilities."""
    return "-".join(
        [
            make_word()
            for _ in range(
                random.choices(
                    population=range(1, 5), cum_weights=[0.6, 0.9, 0.99, 1]
                )[0]
            )
        ]
    )


def make_argument(
    capitalized_prob: float = 0.01,
    style: str = "between_brackets",
    any_number: bool = False,
) -> str:
    """Currently equivalent to a name, wrapped in <_>."""
    styler = argument_styles.get(style)
    if styler is None:
        warn(f"style not defined: {style}, set by default: 'between_brackets'")
        styler = argument_styles["between_brackets"]

    arg = styler(capitalize(make_composed_word(), probability=capitalized_prob))

    if any_number:
        arg += "..."

    return arg


def make_option(
    short: bool = True,
    long: bool = True,
    with_value: bool = False,
    short_capitalized_prob: float = 0.1,
    long_capitalized_prob: float = 0,
    short_separator: str = " ",
    long_separator: str = "=",
    short_long_separator: str = ", ",
    probability_name_cap: float = 0,
    probability_value_cap: float = 0,
    style: str = "between_brackets",
    any_number: bool = False,
):
    """Optional argument generator.

    If short, long and with_value are True, only the short option will be
    generated and returned.

    TODO:
        Possibilities not developed yet:
        - More than a single word for an argument name: [--no-replace-objects]
        - Multiple possibilities: [-p | --paginate | -P | --no-pager]

    Args:
        short (bool, optional):
            Add a short version (single dashed). Defaults to True.
        long (bool, optional):
            Add a long version (double dashed). Defaults to True.
        with_value (bool, optional):
            Add a default value for the . Defaults to False.
        short_capitalized_prob (float, optional):
            Probability of having the argument capitalized. Defaults to 0.1.
        long_capitalized_prob (float, optional):
            Equivalent to short_capitalized_prob for long option. Defaults to 0.
        short_separator (str, optional):
            Separator for the default value in the short option. Defaults to " ".
        long_separator (str, optional):
            Separator for the default value in the long option. Defaults to "=".
        short_long_separator (str, optional):
            Separator between both versions of an argument, i.e.
            -o, --option. The usual values are ", " or " ". Defaults to ",".
        probability_name_cap (float, optional):
            Probability of the name of the option being capitalized. Defaults to 0.
        probability_value_cap (float, optional)
            Probability of the default value of the option being capitalized.
            Defaults to 0.
        style (str, optional). Argument passed to make_argument.
        any_number (bool, optional). Argument passed to make_argument.
    """
    option = ""
    name = capitalize(make_composed_word(), probability=probability_name_cap)
    value = make_argument(
        capitalized_prob=probability_value_cap, style=style, any_number=any_number
    )
    if short:
        option += "-" + capitalize(name[0], short_capitalized_prob)
        if with_value:
            option += short_separator + value
            return option

    if long:
        if short:
            option += short_long_separator
        option += "--" + capitalize(name, long_capitalized_prob)
        if with_value:
            option += long_separator + value
            return option

    return option
