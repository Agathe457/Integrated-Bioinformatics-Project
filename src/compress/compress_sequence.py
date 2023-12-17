import json
import logging

from src.utils.huffman import generic_encode_huffman_binary, generic_decode_huffman_binary

global_huffman = json.load(open("source/global_huffman.encoding", "r"))
global_decoding = {v: k for k, v in global_huffman.items()}


def compress_sequence(sequence, context, encodings, disable_generic=False):
    # Beautiful print encoding
    out = ""

    for index, symbol in enumerate(sequence[context:]):
        code = encodings.get(sequence[index:index + context], {}).get(symbol)
        if code is None:
            code = encodings.get(sequence[index:index + context], {
                "DEFAULT": ""
            }).get("DEFAULT")
            out += code
            # get integer for the symbol
            out += global_huffman.get(symbol)
        else:
            out += code

    # Convert binary string to utf-8 string
    out = [chr(int(out[i:i + 8], 2)) for i in range(0, len(out), 8)]
    # Add the unencoded first context characters
    out = sequence[:context] + "".join(out)

    if not disable_generic:
        out = generic_encode_huffman_binary(out)
    else:
        logging.warning("Compressing without generic encoding.")

    return out


def decompress_sequence(sequence, context, decodings):
    # Decode huffman encoding
    sequence = generic_decode_huffman_binary(sequence)

    # Convert utf-8 string to binary string
    sequence = "".join([bin(ord(char))[2:].zfill(8) for char in sequence])

    # Start sequence with the first context characters
    out = sequence[:context]
    sequence = sequence[context:]

    buffer = ""

    current_decoding = decodings.get(out, global_decoding)

    while sequence:
        buffer += sequence[0]
        sequence = sequence[1:]
        if buffer in current_decoding:
            current_out = current_decoding[buffer]

            if current_out == "DEFAULT":
                buffer = ""
                current_decoding = global_decoding
            else:
                out += current_out
                buffer = ""
                if len(sequence):
                    current_decoding = decodings.get(out[-context:], global_decoding)

    return out
