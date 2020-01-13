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
        if len(line) == 0:
            continue

        try:
            # Use explicit whitespace (avoid 0xA0)
            parts = re.split(r"[ \t]+", line)
            word = parts[0]

            # Skip Julius extras
            parts = [p for p in parts[1:] if p[0] not in ["[", "@"]]

            idx = word.find("(")
            if idx > 0:
                word = word[:idx]

            if "+" in word:
                # Julius format word1+word2
                words = word.split("+")
            else:
                words = [word]

            for word in words:
                # Don't transform silence words
                if transform and (
                    (silence_words is None) or (word not in silence_words)
                ):
                    word = transform(word)

                pronounce = " ".join(parts)

                if word in word_dict:
                    word_dict[word].append(pronounce)
                else:
                    word_dict[word] = [pronounce]
        except Exception as e:
            _LOGGER.warning("read_dict: %s (line %s)", e, i + 1)

    return word_dict
