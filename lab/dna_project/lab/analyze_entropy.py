from collections import defaultdict

from lib.huffman import compute_huffman_encoding
from lib.samples import load_samples_generator
from lib.typedefs import DNA


def analyze_frequencies(data: DNA, sequence_size: int):
    initial_data = data
    stats = defaultdict(int)

    while data:
        stats[data[:sequence_size]] += 1
        data = data[sequence_size:]

    # Order dict by value
    stats = dict(sorted(stats.items(), key=lambda item: item[1], reverse=True))

    # Use huffman encoding to encode the most frequent sequences
    frequencies = list(stats.values())
    sequences = list(stats.keys())
    codes = compute_huffman_encoding(frequencies, sequences)

    # Use the codes dictionary to encode the data
    encoded_data = ""
    data = initial_data

    while data:
        encoded_data += codes[data[:sequence_size]]
        data = data[sequence_size:]

    return encoded_data


if __name__ == '__main__':
    samples = []
    for name, sample in load_samples_generator():
        x = analyze_frequencies(sample, 5)
