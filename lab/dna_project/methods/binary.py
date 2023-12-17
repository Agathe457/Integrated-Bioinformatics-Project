from lib.typedefs import DNA


def compression_function(dna_sequence: DNA) -> DNA:
    conversion_map = {
        "A": "00",
        "C": "01",
        "G": "10",
        "T": "11"
    }

    binary_sequence = ""

    for nucleotide in dna_sequence:
        binary_sequence += conversion_map[nucleotide]

    return ''.join(chr(int(binary_sequence[i:i + 8], 2)) for i in range(0, len(binary_sequence), 8))
