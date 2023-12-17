from lib.typedefs import DNA


def compression_function(dna_sequence: DNA) -> DNA:
    """
    Use rotating run-length encoding to encode a DNA sequence.
    :param dna_sequence: DNA sequence to encode
    :return: encoded DNA sequence
    """

    rotation = ['A', 'C', 'G', 'T']

    current_rotation = 0
    buffer_count = 0
    encoded_sequence = ""
    while dna_sequence:
        if dna_sequence[0] == rotation[current_rotation]:
            buffer_count += 1
            dna_sequence = dna_sequence[1:]
        else:
            encoded_sequence += str(buffer_count)
            buffer_count = 0
            current_rotation = (current_rotation + 1) % 4
    encoded_sequence += str(buffer_count)

    return encoded_sequence
