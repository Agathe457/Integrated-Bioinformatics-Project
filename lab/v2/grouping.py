import os
from collections import defaultdict

from sklearn.cluster import KMeans
from tqdm import tqdm

from src.compress.compress_sequence import compress_sequence
from src.generation.build_encodings import build_codec
from src.generation.constants import ALLOWED_SYMBOLS
from src.io.codec import store_protein_codec, load_protein_codec
from src.io.read_proteins import read_proteins_from_file


def split(protein: str, step: int = 256):
    for i in range(0, len(protein), step):
        yield protein[i: i + step]


distributions = []

COUNT = 100
input_matrix = []

for fasta_file in tqdm(os.listdir("data/proteomes"), desc="Grouping", unit="proteomes"):
    for i, protein in enumerate(read_proteins_from_file("data/proteomes/" + fasta_file)):
        for splitted in split(protein):
            amino_distribution = {
                symbol: 0 for symbol in ALLOWED_SYMBOLS
            }

            for symbol in splitted:
                amino_distribution[symbol] += 1
            # Normalize
            for symbol in amino_distribution:
                amino_distribution[symbol] /= len(splitted)

            input_matrix.append([amino_distribution[symbol] for symbol in ALLOWED_SYMBOLS])
        if i == COUNT:
            break
print("Finished preparing distributions")
os.environ["LOKY_MAX_CPU_COUNT"] = "6"

print()
kmeans = KMeans(n_clusters=40, random_state=0, n_init='auto').fit(input_matrix)

groups = defaultdict(list)

for fasta_file in tqdm(os.listdir("data/proteomes"), desc="Grouping", unit="proteomes"):
    for i, protein in enumerate(read_proteins_from_file("data/proteomes/" + fasta_file)):
        for splitted in split(protein):
            amino_distribution = {
                symbol: 0 for symbol in ALLOWED_SYMBOLS
            }

            for symbol in splitted:
                amino_distribution[symbol] += 1
            # Normalize
            for symbol in amino_distribution:
                amino_distribution[symbol] /= len(splitted)

            # Get the cluster
            cluster = kmeans.predict([[amino_distribution[symbol] for symbol in ALLOWED_SYMBOLS]])[0]

            groups[cluster].append(splitted)

        if i == COUNT:
            break


for group, proteins in groups.items():
    codec = build_codec([proteins], 2)

    store_protein_codec(codec, 2, "group_" + str(group))

for fasta_file in tqdm(os.listdir("data/proteomes"), desc="Grouping", unit="proteomes"):
    total_bps = 0
    c = 0
    for protein in read_proteins_from_file("data/proteomes/" + fasta_file):
        for splitted in split(protein):
            amino_distribution = {
                symbol: 0 for symbol in ALLOWED_SYMBOLS
            }

            for symbol in splitted:
                amino_distribution[symbol] += 1
            # Normalize
            for symbol in amino_distribution:
                amino_distribution[symbol] /= len(splitted)

            cluster = kmeans.predict([[amino_distribution[symbol] for symbol in ALLOWED_SYMBOLS]])[0]

            codec, context = load_protein_codec("group_" + str(group))
            encodings = codec[0]

            try:
                compressed = compress_sequence(splitted, context, encodings)
                bps = ((len(compressed) / 8) / len(splitted)) * 8
                print(bps)
                total_bps += bps
                c += 1
            except:
                pass
    print("Avg bps", total_bps / c)
