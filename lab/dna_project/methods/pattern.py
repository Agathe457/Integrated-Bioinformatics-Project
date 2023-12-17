import abc
from itertools import product

from tqdm import tqdm

from lib.typedefs import DNA


class Pattern(abc.ABC):
    def __init__(self, dna_sequence: DNA):
        self.nucleotide_check = 0
        self.dna = dna_sequence
        self.length = len(dna_sequence)

    @abc.abstractmethod
    def _check(self):
        raise NotImplementedError("This method is a template, please implement it.")

    def get_nucleotide_at(self, index):
        self.nucleotide_check += 1
        return self.dna[index]

    def check(self) -> int:
        self.nucleotide_check = 0
        return self._check() / self.nucleotide_check

    def suggest_at(self, index: int):
        return None


class OneInX(Pattern):
    def __init__(self, dna_sequence: DNA, nucleotide: str, x: int):
        self.nucleotide = nucleotide
        self.x = x
        super().__init__(dna_sequence)

    def _check(self) -> int:
        count = 0
        for index in range(0, self.length, self.x):
            if self.get_nucleotide_at(index) == self.nucleotide:
                count += 1

        return count

    def suggest_at(self, index: int):
        if index % self.x == 0:
            return self.nucleotide


class WheelGoldenRatio(Pattern):
    def __init__(self, dna_sequence: DNA, nucleotide: str):
        super().__init__(dna_sequence)
        self.nucleotide = nucleotide
        self.registered_indexes = []

    def _check(self) -> int:
        count = 0
        golden_ratio = 1.61803398875
        index = 0
        while index < self.length:
            i = round(index)
            self.registered_indexes.append(i)
            if self.get_nucleotide_at(i) == self.nucleotide:
                count += 1
            index += golden_ratio

        return count

    def suggest_at(self, index: int):
        if index in self.registered_indexes:
            return self.nucleotide


def compression_function(dna_sequence: DNA) -> DNA:
    saved_patterns = []
    relatives = {}

    for nucleotide in ["A", "C", "G", "T"]:
        relatives[nucleotide] = dna_sequence.count(nucleotide) / len(dna_sequence)

    # Check for each pattern
    for nucleotide, x in product(["A", "C", "G", "T"], range(2, 20)):
        pattern = OneInX(dna_sequence, nucleotide, x)
        percentage = pattern.check()

        if percentage > relatives[nucleotide]:
            saved_patterns.append(pattern)

    for nucleotide in ["A", "C", "G", "T"]:
        pattern = WheelGoldenRatio(dna_sequence, nucleotide)
        percentage = pattern.check()

        if percentage > relatives[nucleotide]:
            saved_patterns.append(pattern)

    print("Launching recomposition...")

    recomposed_sequence = ""

    for index in tqdm(range(len(dna_sequence)), desc="Recomposition", unit="nucleotide"):
        distribution = []
        for pattern in saved_patterns:
            nucleotide = pattern.suggest_at(index)
            if nucleotide:
                distribution.append(nucleotide)

        most_frequent = max(set(distribution), key=distribution.count) if distribution else None

        if most_frequent:
            recomposed_sequence += most_frequent
        else:
            recomposed_sequence += max(relatives, key=relatives.get)

    # Compute delta
    delta = 0

    for index in range(len(dna_sequence)):
        if dna_sequence[index] != recomposed_sequence[index]:
            delta += 1

    print(f"Lost: {delta / len(dna_sequence)}")

    return dna_sequence
