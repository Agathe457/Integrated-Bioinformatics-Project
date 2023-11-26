from typing import List, Generator, Dict

from src.generation.generate_encoding import generate_encoding_from_proteins


def build_codec(sources: List[Generator[str, None, None]], context: int) -> List[Dict]:
    """
    Build a codec from a list of sources.

    :param sources: The sources to build the codec from
    :param context: The context to use
    :return: The codec
    """
    codec = []

    for source in sources:
        encodings = generate_encoding_from_proteins(source, context)
        codec.append(encodings)

    return codec
