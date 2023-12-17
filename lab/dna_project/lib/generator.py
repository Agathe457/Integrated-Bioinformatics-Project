import random
from typing import Iterable

from lib.constants import NUCLEOTIDES
from lib.typedefs import DNA


def generate_synthetic_dna(size: int, repartition: Iterable[int] = None) -> DNA:
    """
    A method that generates a synthetic DNA strand. The frequencies
    of each nucleotide is based on the repartition argument.
    :param size: The length of the DNA strand to produce.
    :param repartition: The relative frequency of each nucleotide in the following
        order A - T - G - C.
    :return: The random synthetic DNA strand
    """

    if repartition is None:
        repartition = [1, 1, 1, 1]

    assert len(repartition) == 4, "The repartition arguments must be in the form [int, int, int, int]"

    buffer = ""

    for _ in range(size):
        buffer += random.choices(
            NUCLEOTIDES,
            weights=repartition,
            k=1
        )[0]

    return buffer
