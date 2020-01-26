"""Utility methods for rhasspyasr"""
import logging
import re
import typing

_LOGGER = logging.getLogger(__name__)


def read_dict(
    dict_file: typing.Iterable[str],
    word_dict: typing.Optional[typing.Dict[str, typing.List[str]]] = None,
    transform: typing.Optional[typing.Callable[[str], str]] = None,
    silence_words: typing.Optional[typing.Set[str]] = None,
) -> typing.Dict[str, typing.List[str]]:
    """
    Loads a CMU/Julius word dictionary, optionally into an existing Python dictionary.
    """
    if word_dict is None:
        word_dict = {}

    for i, line in enumerate(dict_file):
        line = line.strip()
        if not line:
            continue

        try:
            # Use explicit whitespace (avoid 0xA0)
            word, *parts = re.split(r"[ \t]+", line)

            # Skip Julius extras
            pronounce = " ".join(p for p in parts if p[0] not in {"[", "@"})

            word = word.split("(")[0]
            # Julius format word1+word2
            words = word.split("+")

            for word in words:
                # Don't transform silence words
                if transform and (
                    (silence_words is None) or (word not in silence_words)
                ):
                    word = transform(word)

                if word in word_dict:
                    word_dict[word].append(pronounce)
                else:
                    word_dict[word] = [pronounce]
        except Exception as e:
            _LOGGER.warning("read_dict: %s (line %s)", e, i + 1)

    return word_dict
