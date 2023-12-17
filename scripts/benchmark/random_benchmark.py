import os
import random
from tqdm import tqdm
from src.compress.compress_sequence import compress_sequence
from src.generation.generate_encoding import generate_encoding_from_proteins
from src.io.read_proteins import read_proteins_from_file

# Define the output CSV file path
output_csv_path = "out/random.csv"

# Create the 'out' folder if it doesn't exist
if not os.path.exists("out"):
    os.mkdir("out")

# Reset the CSV file by writing the header
with open(output_csv_path, "w") as f:
    f.write("proteome,compression_ratio,bits_per_symbol,compression_speed(bytes/s),context\n")

# Define the folder containing proteome data
folder = "data/proteomes"

# Iterate over different context values (0 to 4)
for context in range(5):
    # For every FASTA file in the 'data/proteomes' folder, compress and decompress it
    for fasta_file in tqdm(os.listdir(folder), desc="Benchmarking", unit="proteomes"):
        try:
            # Select a random subset of 500 proteins from the FASTA file
            source = random.choices(list(read_proteins_from_file(os.path.join(folder, fasta_file))), k=500)
            source_2 = []

            # Shuffle the amino acid sequences within each protein
            for prot in source:
                x = list(prot)
                random.shuffle(x)
                source_2.append(''.join(x))

            # Generate encodings for the shuffled protein sequences
            encodings = generate_encoding_from_proteins(source_2, context)

            compression_ratio = 0
            bits_per_symbol = 0
            count = 0
            time_taken = 0
            total_length = 0

            # Select a random subset of 10 proteins from the FASTA file
            source_3 = random.choices(list(read_proteins_from_file(os.path.join(folder, fasta_file))), k=10)
            source_4 = []

            # Shuffle the amino acid sequences within each protein
            for prot in source_3:
                x = list(prot)
                random.shuffle(x)
                source_4.append(''.join(x))

            for protein in source_4:
                count += 1
                s = compress_sequence(protein, context, encodings)
                compression_ratio += (len(s) / 8) / len(protein)
                bits_per_symbol += (len(s) / 8) / len(protein) * 8
                total_length += len(protein)

                # Stop after processing 500 proteins
                if count == 500:
                    break

            avg_compression_ratio = compression_ratio / count
            avg_bits_per_symbol = bits_per_symbol / count

            # Write the results to the CSV file
            with open(output_csv_path, "a") as output_csv:
                output_csv.write(fasta_file.replace(".fasta", "") + "," + str(avg_compression_ratio) + "," + str(
                    avg_bits_per_symbol) + "," + str(time_taken) + "," + str(context) + "\n")
        except IndexError:
            pass
