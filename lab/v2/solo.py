import json
import os

from tqdm import tqdm

from src.compress.compress_sequence import compress_sequence
from src.generation.build_encodings import build_codec
from src.io.read_proteins import read_proteins_from_file


def split(protein: str, step: int = 256):
    for i in range(0, len(protein), step):
        yield protein[i: i + step]


distributions = []

COUNT = 10000
input_matrix = []

encodings = []

previous_codec = None
encoding = None

for fasta_file in tqdm(os.listdir("data/proteomes"), desc="Grouping", unit="proteomes"):
    train_prot = []

    for i, protein in enumerate(read_proteins_from_file("data/proteomes/" + fasta_file)):
        if i == 100:
            break

        train_prot.append(protein)

    context = 2
    codec = build_codec([train_prot], context)
    encoding = json.loads(json.dumps(codec[0]))

    t_bps = 0
    x = 0
    for i, protein in enumerate(read_proteins_from_file("data/proteomes/" + fasta_file)):
        if i <= 100:
            continue

        try:
            bps = ((len(compress_sequence(protein, context, encoding)) / 8) / len(protein)) * 8
            t_bps += bps
            x += 1
        except:
            pass
        if i > 1000:
            break

    print(t_bps/x)