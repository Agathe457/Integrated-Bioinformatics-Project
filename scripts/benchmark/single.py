import math
import os
import random
from collections import defaultdict
from tqdm import tqdm
import matplotlib.pyplot as plt

from src.compress.compress_sequence import compress_sequence
from src.generation.generate_encoding import generate_encoding_from_proteins
from src.io.read_proteins import read_proteins_from_file

# Loop through different contexts
for context in range(6):
    folder = "data/proteomes"

    # Initialize dictionaries for various statistics
    total_per_proteomes = defaultdict(int)
    total_per_proteomes_1_prct_changed = defaultdict(int)
    total_per_proteomes_5_prct_changed = defaultdict(int)
    total_per_proteomes_10_prct_changed = defaultdict(int)
    total_per_proteomes_20_prct_changed = defaultdict(int)
    total_per_proteomes_50_prct_changed = defaultdict(int)
    total_per_proteomes_75_prct_changed = defaultdict(int)
    total_per_proteomes_100_prct_changed = defaultdict(int)
    shannon_entropy = defaultdict(lambda: defaultdict(int))

    # Create a mapping for percentage change
    mapping = {
        0: total_per_proteomes,
        1: total_per_proteomes_1_prct_changed,
        5: total_per_proteomes_5_prct_changed,
        10: total_per_proteomes_10_prct_changed,
        20: total_per_proteomes_20_prct_changed,
        50: total_per_proteomes_50_prct_changed,
        75: total_per_proteomes_75_prct_changed,
        100: total_per_proteomes_100_prct_changed
    }

    count_per_proteomes = defaultdict(int)

    # Loop through every fasta file in data/proteomes, compress and decompress it
    for fasta_file in tqdm(os.listdir(folder), desc="Benchmarking", unit="proteomes"):
        for i, protein in enumerate(read_proteins_from_file(folder + "/" + fasta_file)):
            if i == 10:
                break

            def _fake_generator():
                yield protein

            # Generate encodings from proteins
            encodings = generate_encoding_from_proteins(_fake_generator(), context)
            decodings = {key: {v: k for k, v in value.items()} for key, value in encodings.items()}

            # Make a copy of the original protein
            copy = protein

            for prct in [0, 1, 5, 10, 20, 50, 75, 100]:
                protein = list(copy)
                # Randomly change a percentage of the protein
                for _ in range(len(protein) * prct // 100):
                    protein[random.randint(0, len(protein) - 1)] = random.choice("ACDEFGHIKLMNPQRSTVWY")

                protein = "".join(protein)

                # Compress the sequence and calculate compression rate and bits per symbol
                compressed_sequence = compress_sequence(protein, context, encodings)
                compression_rate = (len(compressed_sequence) / 8) / len(protein)
                bps = 8 * compression_rate

                mapping[prct][fasta_file] += bps

                # Calculate Shannon entropy
                shannon_entropy[prct][fasta_file] += -sum([protein.count(aa) / len(protein) * math.log2(protein.count(aa) / len(protein)) for aa in set(protein)])

            count_per_proteomes[fasta_file] += 1

    # Calculate the average bits per symbol for each percentage of changed amino acids
    for key, value in mapping.items():
        for k, v in value.items():
            value[k] = v / count_per_proteomes[k]

    # Calculate the average Shannon entropy for each percentage of changed amino acids
    for key in mapping.keys():
        for k, v in shannon_entropy[key].items():
            shannon_entropy[key][k] = v / count_per_proteomes[k]

    # Plot the evolution of bits per symbol per percentage of changed amino acids (average over all proteomes)
    plt.plot(list(mapping.keys()), [sum(value.values()) / len(value.values()) for value in mapping.values()],
             label="BPS for context " + str(context), alpha=0.8)
    plt.xlabel("Percentage of changed amino acids")
    plt.ylabel("Bits per symbol")
    plt.legend()
    # Make the plot visually suited for a research paper
    plt.tight_layout()
    # Add grid
    plt.grid()
    plt.savefig("bps_per_prct_changed.png", dpi=300)
    plt.show()
