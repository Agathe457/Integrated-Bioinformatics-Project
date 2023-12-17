from math import log2

from lib.samples import load_samples_generator
from lib.typedefs import DNA


def analyze_entropy(data: DNA, sequence_size: int):
    groups = [
        data[i:i + sequence_size]
        for i in range(0, len(data), sequence_size)
    ]

    entropy = sum(
        [
            (groups.count(group) / len(groups)) *  # p(x)
            log2(groups.count(group) / len(groups))  # log2(p(x))
            for group in set(groups)
        ]
    ) * -1

    group_count = len(set(groups))
    return entropy, round(len(groups) * entropy), (len(groups) * entropy + group_count * log2(group_count)) / (len(data) * 8)


if __name__ == '__main__':
    samples = []
    for name, sample in load_samples_generator():
        for i in range(1, 7):
            x = analyze_entropy(sample, i)
            print(f"{name} - {i} - {x}")
