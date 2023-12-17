import heapq
from collections import defaultdict

from lib.typedefs import DNA

GROUP_SIZE = 3


class HuffmanNode:
    def __init__(self, symbol, freq):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(freq_dict):
    heap = [HuffmanNode(sym, freq) for sym, freq in freq_dict.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged_node = HuffmanNode(None, left.freq + right.freq)
        merged_node.left = left
        merged_node.right = right
        heapq.heappush(heap, merged_node)

    return heap[0]


def generate_huffman_codes(node, code, result):
    if node.symbol is not None:
        result[node.symbol] = code
    if node.left:
        generate_huffman_codes(node.left, code + "0", result)
    if node.right:
        generate_huffman_codes(node.right, code + "1", result)


def huffman_coding(freq_dict):
    root = build_huffman_tree(freq_dict)
    huffman_codes = {}
    generate_huffman_codes(root, "", huffman_codes)
    return huffman_codes


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


def x(y):
    """
        Check most common groups of nucleotides in subsequences of DELTA_SIZE.
        Then replace the most common groups with a single letter.
        """
    groups = [
        y[i:i + GROUP_SIZE]
        for i in range(0, len(y), GROUP_SIZE)
    ]

    stats = defaultdict(int)

    for group in groups:
        stats[group] += 1
    # order dict by value
    stats = dict(sorted(stats.items(), key=lambda item: item[1], reverse=True))
    print(stats)
    codes = huffman_coding(stats)
    # use the codes dictionary to encode the data
    encoded_data = ""

    for group in groups:
        encoded_data += codes[group]

    # convert the string sequence to binary then to utf-8
    encoded_string = _binary_to_utf8(encoded_data)

    return encoded_string


def compression_function(dna_sequence: DNA) -> DNA:
    a = ""
    for i in range(0, len(dna_sequence), 500):
        a += x(dna_sequence[i:i + 500])

    return a