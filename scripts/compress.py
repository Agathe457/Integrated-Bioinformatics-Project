import time
from collections import defaultdict

from src.compress.compress_sequence import compress_sequence, decompress_sequence
from src.io.codec import load_protein_codec
from src.io.read_proteins import read_proteins_from_file

codec, context = load_protein_codec("test")

a = defaultdict(int)
x = 0
avg = 0
t = 0

start_time = time.time()
encodings = codec[0]


def build_decodings(encodings: dict, context: int):
    decoding = {}

    for key, value in encodings.items():
        if type(value) == str:
            decoding[value] = key
        else:
            decoding[key] = build_decodings(value, context)

    return decoding


decodings = build_decodings(encodings, context)

for protein in read_proteins_from_file("test_data/leo.tsv"):
    x += 1
    s = compress_sequence(protein, context, encodings)
    d = decompress_sequence(s, context, decodings)
    print(protein[:10])
    print(d[:10])
    avg += len(s) / len(protein)
    t += len(protein)

end_time = time.time()

# Compute bytes / second
compression_speed = t / (end_time - start_time)

print("Average compression ratio: ", avg / x)
print("Compression speed: ", compression_speed, " bytes / second")
