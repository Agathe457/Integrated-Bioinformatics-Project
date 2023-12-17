from collections import defaultdict

from lib.huffman import compute_huffman_encoding
from lib.typedefs import DNA

SEQUENCE_SIZE = 7


def compression_function(dna_sequence: DNA) -> DNA:
    stats = defaultdict(int)
    data = dna_sequence

    while data:
        stats[data[:SEQUENCE_SIZE]] += 1
        data = data[SEQUENCE_SIZE:]

    # Order dict by value
    stats = dict(sorted(stats.items(), key=lambda item: item[1], reverse=True))

    # Use huffman encoding to encode the most frequent sequences
    frequencies = list(stats.values())
    sequences = list(stats.keys())
    codes = compute_huffman_encoding(frequencies, sequences)

    # Use the codes dictionary to encode the data
    encoded_data = ""
    data = dna_sequence

    while data:
        encoded_data += codes[data[:SEQUENCE_SIZE]]
        data = data[SEQUENCE_SIZE:]

    # Convert the string sequence to binary then to utf-8
    encoded_string = _binary_to_utf8(encoded_data)
    return encoded_string


def _binary_to_utf8(binary_sequence: str) -> str:
    """
    Convert a binary sequence to utf-8.
    :param binary_sequence: binary sequence to convert
    :return: utf-8 sequence
    """
    utf8_sequence = ""
    for i in range(0, len(binary_sequence), 8):
        utf8_sequence += chr(int(binary_sequence[i:i + 8], 2))
    return utf8_sequence
