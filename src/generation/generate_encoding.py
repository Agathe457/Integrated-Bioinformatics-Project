from collections import defaultdict
from typing import Generator

from src.generation.constants import ALLOWED_SYMBOLS
from src.utils.huffman import get_encoding_from_freq_map


def _create_frequency_table(context: int):
    if context == 0:
        return int
    else:
        return lambda: defaultdict(_create_frequency_table(context - 1))


def _recurse(freq_map: dict, encoding: dict, context: int, depth: int = 0):
    """
    The recursive function that generates the encoding from the frequency map.

    :param freq_map: The frequency map to generate the encoding from
    :param encoding: The encoding to update
    :param symbols: The set of symbols to include in the encoding
    """
    if freq_map and type(list(freq_map.values())[0]) == int:
        encoding.update(get_encoding_from_freq_map({
            **freq_map,
            **{key: 1 for key in ALLOWED_SYMBOLS if key not in freq_map}
        }))
    else:
        for symbol in ALLOWED_SYMBOLS:
            if symbol in freq_map:
                _recurse(freq_map[symbol], encoding[symbol], context, depth + 1)
            elif context == depth + 1:
                _recurse({
                    key: 1 for key in ALLOWED_SYMBOLS
                }, encoding[symbol], context, depth + 1)
            else:
                _recurse({}, encoding[symbol], context, depth + 1)


def generate_encoding_from_proteins(proteins: Generator[str, None, None], context: int):
    frequency_table = defaultdict(_create_frequency_table(context))

    for protein in proteins:
        for index, symbol in enumerate(protein[context:]):
            access = frequency_table

            for i in range(context):
                access = access[protein[index + context - i - 1]]

            access[symbol] += 1

    encodings = defaultdict(_create_frequency_table(context))

    # Get huffman encoding tree for each
    _recurse(frequency_table, encodings, context)

    return encodings
