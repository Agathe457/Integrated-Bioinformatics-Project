import json
import os
import random
from collections import defaultdict

from tqdm import tqdm

from src.compress.compress_sequence import compress_sequence
from src.generation.build_encodings import build_codec
from src.io.read_proteins import read_proteins_from_file
from src.utils.huffman import get_encoding_from_freq_map

# For every fasta file in data/proteomes, compress it and decompress it
SOURCE = "data/proteomes"
context = 3

proteins = []

for fasta_file in tqdm(os.listdir(SOURCE), desc="Extracting proteins", unit="proteomes"):
    a = 0

    try:
        proteins += random.choices(list(read_proteins_from_file(SOURCE + "/" + fasta_file)), k=1000)
    except Exception as e:
        print(f"\nCould not process {fasta_file}, due to: {e}")

encodings = build_codec([proteins], context)[0]

# Create out folder if it doesn't exist
if not os.path.exists("out"):
    os.mkdir("out")

output_csv_path = "out/benchmark.csv"

# Reset csv
with open(output_csv_path, "w") as f:
    f.write("proteome,compression_ratio,bits_per_symbol,compression_speed(bytes/s)\n")

freq = defaultdict(int)

# For every fasta file in data/proteomes, compress it and decompress it
for fasta_file in tqdm(os.listdir(SOURCE), desc="Generating frequency map for encoded strings", unit="proteomes"):
    x = 0

    for protein in read_proteins_from_file("data/proteomes/" + fasta_file):
        for symbol in compress_sequence(protein, context, encodings, disable_generic=True):
            freq[symbol] += 1

        x += 1

        if x == 100:
            break

if os.environ.get("DEBUG", True):
    import matplotlib.pyplot as plt

    plt.bar(list(freq.keys()), list(freq.values()))
    plt.show()

# store to source/generic.encoding (new file)
with open("source/generic.encoding", "w") as f:
    f.write(json.dumps(get_encoding_from_freq_map(freq)))

print("Generic encoding has been generated.")