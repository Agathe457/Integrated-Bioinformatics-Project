from src.generation.build_encodings import build_codec
from src.io.codec import store_protein_codec
from src.io.read_proteins import read_proteins_from_file

g1 = read_proteins_from_file("test_data/leo.tsv")

codec = build_codec([g1], 3)

store_protein_codec(codec, 3, "test")

