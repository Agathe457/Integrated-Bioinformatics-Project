import json
import math
import os

from tqdm import tqdm

from src.compress.compress_sequence import compress_sequence, decompress_sequence
from src.generation.generate_encoding import generate_encoding_from_proteins
from src.io.read_proteins import read_proteins_from_file

# Define the path for the output CSV file
output_csv_path = "out/results.csv"

# Create the 'out' folder if it doesn't exist
if not os.path.exists("out"):
    os.mkdir("out")

# Reset the contents of the CSV file
with open(output_csv_path, "w") as f:
    f.write("proteome,compression_ratio,bits_per_symbol,compression_speed(bytes/s),context\n")

# Define the folder where the proteome data is located
folder = "data/proteomes"

# Iterate through different context values (3 to 4)
for context in range(3, 5):
    # Iterate through each fasta file in the 'data/proteomes' folder for benchmarking
    for fasta_file in tqdm(os.listdir(folder), desc="Benchmarking", unit="proteomes"):
        try:
            # Generate encodings for a subset of proteins
            encodings = generate_encoding_from_proteins(
                list(read_proteins_from_file(os.path.join(folder, fasta_file)))[:500], context)

            # Dump the encodings to a JSON file (for debugging or analysis purposes)
            json.dump(encodings, open("x.json", "w"))

            # Initialize variables for metrics
            compression_ratio = 0
            bits_per_symbol = 0
            count = 0
            total_length = 0

            # Create reverse encodings for decompression
            decodings = {key: {v: k for k, v in value.items()} for key, value in encodings.items()}

            # Initialize a variable for tracking time taken (not calculated in this code)
            time_taken = 0

            # Iterate through a subset of proteins from the file
            for protein in list(read_proteins_from_file(os.path.join(folder, fasta_file)))[:500]:
                count += 1
                # Compress the protein sequence
                s = compress_sequence(protein, context, encodings)

                # Decompress the compressed sequence
                ad = decompress_sequence(s, context, decodings)

                # Calculate compression ratio
                compression_ratio += (len(s) / 8) / len(protein)

                # Calculate bits per symbol
                x = (len(s) / 8) / len(protein) * 8
                bits_per_symbol += x

                # Calculate total length of proteins
                total_length += len(protein)

            # Calculate average compression ratio and average bits per symbol
            avg_compression_ratio = compression_ratio / count
            avg_bits_per_symbol = bits_per_symbol / count

            # Print the average bits per symbol (for debugging or analysis purposes)
            print(avg_bits_per_symbol)

            # Write the results to the CSV file
            with open(output_csv_path, "a") as output_csv:
                output_csv.write(fasta_file.replace(".fasta", "") + "," + str(avg_compression_ratio) + "," + str(
                    avg_bits_per_symbol) + "," + str(time_taken) + "," + str(context) + "\n")

        # Handle the case where an IndexError occurs (you might want to log this)
        except IndexError:
            pass
