import json
import os
from collections import defaultdict

from tqdm import tqdm

from src.generation.build_encodings import build_codec
from src.io.codec import store_protein_codec
from src.io.read_proteins import read_proteins_from_file
from src.utils.huffman import get_encoding_from_freq_map

g1 = read_proteins_from_file("test_data/leo.tsv")

codec = build_codec([g1], 2)

store_protein_codec(codec, 2, "test")
folder = "data/proteomes"

freq = defaultdict(int)

for fasta_file in tqdm(os.listdir(folder), desc="Building freq", unit="proteomes"):
    for i, protein in enumerate(read_proteins_from_file(folder + "/" + fasta_file)):
        for a in protein:
            freq[a] += 1

        if i == 1000:
            break

if os.environ.get("DEBUG", True):
    import matplotlib.pyplot as plt

    plt.bar(list(freq.keys()), list(freq.values()))
    plt.show()

encoding = get_encoding_from_freq_map(freq)
json.dump(encoding, open("global_huffman.encoding", "w"))
