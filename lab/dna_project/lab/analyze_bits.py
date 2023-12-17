from collections import defaultdict

from lib.huffman import compute_huffman_encoding
from lib.samples import load_samples_generator
from lib.typedefs import DNA

CONV = {
    "A": "00",
    "C": "01",
    "G": "10",
    "T": "11"
}


def analyze_bits(data: DNA, sequence_size: int):
    x = ""

    for nucleotide in data:
        x += CONV[nucleotide]

    # Check each 8 substring, if next 8 substring is the same, then
    # skip it and append 0 to the result else append 1 to the result
    # but include the substring in the result
    result = ""

    i = 0

    duplicate_count = 0


    while i < len(x):
        if i + sequence_size < len(x) and x[i:i + sequence_size] == x[i + sequence_size:i + sequence_size * 2]:
            result += "0"
            i += sequence_size
            duplicate_count += 1
        else:
            result += "1"
            result += x[i:i + sequence_size]
            i += sequence_size
    print(duplicate_count / len(x) * 100)
    return result


if __name__ == '__main__':
    samples = []
    for name, sample in load_samples_generator():
        x = analyze_bits(sample,8)
        print(len(x), len(sample)*2)
