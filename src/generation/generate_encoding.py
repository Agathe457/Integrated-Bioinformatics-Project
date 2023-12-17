import json
from collections import defaultdict
from typing import Generator

from src.utils.huffman import get_encoding_from_freq_map


def generate_encoding_from_proteins(proteins: Generator[str, None, None], context: int):
    frequency_table = defaultdict(lambda: defaultdict(int))

    for protein in proteins:
        for index, symbol in enumerate(protein[context:]):
            frequency_table[protein[index:index + context]][symbol] += 1

    encodings = {}

    for prefix in frequency_table:
        encodings[prefix] = get_encoding_from_freq_map({
            **frequency_table[prefix],
            "DEFAULT": 1
        })

    return json.loads(json.dumps(encodings))
