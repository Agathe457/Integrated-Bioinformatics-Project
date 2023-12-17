import os
import time
from collections import defaultdict
from math import log

import matplotlib.pyplot as plt
from tqdm import tqdm

from src.compress.compress_sequence import compress_sequence
from src.generation.generate_encoding import generate_encoding_from_proteins
from src.io.read_proteins import read_proteins_from_file

# Create the 'out' folder if it doesn't exist
if not os.path.exists("out"):
    os.mkdir("out")

output_csv_path = "out/benchmark.csv"

# Initialize statistics dictionaries
stats = defaultdict(list)
context = 3

# Benchmarking process for protein compression and decompression
for fasta_file in tqdm(os.listdir("data/proteomes"), desc="Benchmarking", unit="proteomes"):
    compression_ratio = 0
    bits_per_symbol = 0
    count = 0
    time_taken = 0
    total_length = 0
    start_time = time.time()
    encodings = generate_encoding_from_proteins(
        list(read_proteins_from_file(os.path.join("data/proteomes", fasta_file)))[:500], context)

    for protein in read_proteins_from_file("data/proteomes/" + fasta_file):

        count += 1
        compressed_sequence = compress_sequence(protein, context, encodings)
        compression_ratio += len(compressed_sequence) / len(protein)
        bits_per_symbol += len(compressed_sequence) / len(protein) * 8 / 10
        total_length += len(protein)
        power_of_2_length = round(log(len(protein), 2))
        stats[power_of_2_length].append(len(compressed_sequence) / len(protein) * 8 / 10)

        # Stop after processing 1000 proteins
        if count == 1000:
            break

# Remove data if there are less than 70 samples
for power_of_2_length in list(stats.keys()):
    if len(stats[power_of_2_length]) < 70:
        del stats[power_of_2_length]

# Plot the average bits per symbol for each power of 2
plt.style.use('ggplot')
plt.xlabel("Power of 2 of the length of the protein")
plt.ylabel("Average bits per symbol")
plt.title("Average bits per symbol for each power of 2 of the length of the protein")
average_bits_per_symbol = [sum(stats[power_of_2_length]) / len(stats[power_of_2_length]) for power_of_2_length in
                           stats.keys()]
plt.plot(average_bits_per_symbol)

# Increase the size of the plot
plt.gcf().set_size_inches(10, 5)

# Display the plot
plt.show()
