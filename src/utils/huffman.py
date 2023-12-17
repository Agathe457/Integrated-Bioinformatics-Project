import heapq
import json
from collections import defaultdict


class HuffmanNode:
    """
        A node in the huffman tree, the huffman tree is used to encode the data
        of a file in a way that the most frequent characters are encoded with the
        least amount of bits, and the least frequent characters are encoded with
        the most amount of bits.
    """

    def __init__(self, value, freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        """ A useful operator to enable node comparison"""
        return self.freq < other.freq


def encoding_to_decoding_codes(codes: dict):
    return {
        value: key for value, key in codes.items()
    }


# Load generic codes from source/generic.encoding (these are codes generated
# from the frequencies of all amino acids in 100 random proteomes), supposed
# to be a representative sample.
generic_codes = json.load(open("source/generic.encoding", "r"))
generic_decoding_codes = encoding_to_decoding_codes(generic_codes)


def build_huffman_tree(freq_map: dict):
    """
    Builds a huffman tree from a dictionary of value: frequency/nb of occurrence
    :param freq_map: The dictionary
    :return: The root of the tree.
    """
    heap = [HuffmanNode(value, freq) for value, freq in freq_map.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]


def build_huffman_codes(node, current_code, huffman_codes):
    """ A recursive function to create the huffman encoding from the tree. """
    if node is None:
        return
    if node.value is not None:
        huffman_codes[node.value] = current_code
    build_huffman_codes(node.left, current_code + "0", huffman_codes)
    build_huffman_codes(node.right, current_code + "1", huffman_codes)


def get_encoding_from_freq_map(freq_map: dict):
    """ Returns the huffman encoding for a given tree """
    root = build_huffman_tree(freq_map)

    codes = {}
    build_huffman_codes(root, "", codes)

    return codes


def convert_to_huffman_binary(data: list, huffman_codes: dict = None):
    """
    Converts an iterable input into a binary output using the specified huffman codes.
    """
    if huffman_codes is None:
        freq_map = defaultdict(int)
        for num in data:
            freq_map[num] += 1

        root = build_huffman_tree(freq_map)

        huffman_codes = {}
        build_huffman_codes(root, "", huffman_codes)

    binary_list = ""

    for num in data:
        binary_list += huffman_codes[num]

    return binary_list


def generic_encode_huffman_binary(data: list):
    """ Uses the generic tables loaded above to encode a list"""
    return convert_to_huffman_binary(data, generic_codes)


def decode_huffman_binary(data: str, huffman_codes: dict):
    """ Decodes a string of 1 and 0 using the specified huffman codes"""
    decoded = ""
    code = ""
    for bit in data:
        code += bit
        if code in huffman_codes:
            decoded += huffman_codes[code]
            code = ""
    return decoded


def generic_decode_huffman_binary(data: str):
    """ Uses the generic tables loaded above to decode a string of 1 and 0"""
    return decode_huffman_binary(data, generic_decoding_codes)
