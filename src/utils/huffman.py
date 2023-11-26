import heapq
import json
from collections import defaultdict


class HuffmanNode:
    def __init__(self, value, freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


generic_codes = json.load(open("source/generic.encoding", "r"))


def build_huffman_tree(freq_map):
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
    if node is None:
        return
    if node.value is not None:
        huffman_codes[node.value] = current_code
    build_huffman_codes(node.left, current_code + "0", huffman_codes)
    build_huffman_codes(node.right, current_code + "1", huffman_codes)


def get_encoding_from_freq_map(freq_map):
    root = build_huffman_tree(freq_map)

    huffman_codes = {}
    build_huffman_codes(root, "", huffman_codes)

    return huffman_codes


def convert_to_huffman_binary(data: list, huffman_codes: dict = None):
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
    return convert_to_huffman_binary(data, generic_codes)


def decode_huffman_binary(data: str, huffman_codes: dict):
    decoded = ""
    code = ""
    for bit in data:
        code += bit
        if code in huffman_codes:
            decoded += huffman_codes[code]
            code = ""

    return decoded


def generic_decode_huffman_binary(data: str):
    # Load huffman codes from source/generic.encoding
    # Reverse the huffman codes
    huffman_codes = {value: key for key, value in generic_codes.items()}
    return decode_huffman_binary(data, huffman_codes)
