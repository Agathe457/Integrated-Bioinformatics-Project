from io import BytesIO

from lib.typedefs import DNA


def compression_function(dna_sequence: DNA) -> DNA:
    """
    GZIP compression function.
    :param dna_sequence:
    :return:
    """

    # Use gzip to compress the data
    import gzip

    binary_buffer = BytesIO()

    # Convert the string sequence to binary then to utf-8
    with gzip.open(binary_buffer, mode="wb") as f:
        f.write(dna_sequence.encode("utf-8"))

    return binary_buffer.getvalue()
