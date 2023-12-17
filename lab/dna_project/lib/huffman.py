from queue import PriorityQueue


class Node:
    def __init__(self, character, frequency):
        self.character = character
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency


def compute_huffman_encoding(frequencies, sequences):
    # Create a priority queue (min-heap) to store nodes
    pq = PriorityQueue()

    # Create a leaf node for each character and add it to the priority queue
    for i in range(len(frequencies)):
        pq.put(Node(sequences[i], frequencies[i]))

    # Build the Huffman tree
    while pq.qsize() > 1:
        left = pq.get()
        right = pq.get()
        # Create a new internal node with the sum of frequencies
        top = Node(None, left.frequency + right.frequency)
        top.left = left
        top.right = right
        # Add the new node back to the priority queue
        pq.put(top)

    # Create a dictionary to store Huffman codes for each character
    codes = {}
    root = pq.get()
    build_huffman_codes(root, "", codes)

    return codes


def build_huffman_codes(node, code, codes):
    if node is None:
        return
    if node.character is not None:
        codes[node.character] = code
    build_huffman_codes(node.left, code + "0", codes)
    build_huffman_codes(node.right, code + "1", codes)
