import os
from typing import Generator

from lib.constants import SAMPLES_FOLDER, SYNTHETIC_SAMPLES, NUCLEOTIDES
from lib.generator import generate_synthetic_dna
from lib.typedefs import DNA


def load_samples_generator() -> Generator[DNA, None, None]:
    samples = os.listdir(SAMPLES_FOLDER)

    for sample in samples:
        with open(SAMPLES_FOLDER / sample, 'r') as sample_io:
            yield sample, ''.join(filter(
                lambda x: x in NUCLEOTIDES,
                sample_io.read().upper()
            ))


def load_synthetic_samples_generator() -> Generator[DNA, None, None]:
    for (size, repartition) in SYNTHETIC_SAMPLES:
        yield str(f"SYNTHETIC-{size}-{';'.join(map(str, repartition))}"), generate_synthetic_dna(size,
                                                                                                 repartition).upper()
