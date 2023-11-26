from src.utils.huffman import generic_encode_huffman_binary, generic_decode_huffman_binary


def compress_sequence(sequence, context, encodings):
    # Beautiful print encoding
    out = ""

    for index, symbol in enumerate(sequence[context:]):
        access = encodings

        for i in range(context):
            access = access[sequence[index - context + i]]
        out += str(access[symbol])

    # Convert binary string to utf-8 string
    out = [chr(int(out[i:i + 8], 2)) for i in range(0, len(out), 8)]

    # Add the unencoded first context characters
    out = sequence[:context] + "".join(out)

    out = generic_encode_huffman_binary(out)

    return out


def decompress_sequence(sequence, context, decodings):
    def _get_decodings_recursively_from_last_characters(decodings, characters):
        if len(characters) == 1:
            return decodings[characters[0]]
        else:
            return _get_decodings_recursively_from_last_characters(decodings[characters[0]], characters[1:])

    # Decode huffman encoding
    sequence = generic_decode_huffman_binary(sequence)

    # Start sequence with the first context characters
    out = sequence[:context]

    # Convert utf-8 string to binary string
    sequence = "".join([bin(ord(char))[2:].zfill(8) for char in sequence[context:]])

    # Remove the first context characters
    sequence = sequence[context:]

    buffer = ""

    current_decodings = _get_decodings_recursively_from_last_characters(decodings, out)

    while sequence:
        buffer += sequence[0]
        sequence = sequence[1:]

        if buffer in current_decodings:
            out += current_decodings[buffer]
            buffer = ""
            current_decodings = _get_decodings_recursively_from_last_characters(decodings, out[-context:])
    return out
