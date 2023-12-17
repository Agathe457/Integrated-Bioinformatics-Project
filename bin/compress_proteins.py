import argparse

from tqdm import tqdm

from src.compress.binary_utf8 import binary_string_to_utf8
from src.compress.compress_sequence import compress_sequence
from src.io.codec import load_protein_codec
from src.io.read_proteins import read_proteins_from_file


def main():
    parser = argparse.ArgumentParser(description='Compress AA sequences from input files')
    parser.add_argument('input_files', nargs='+', help='Input file paths')
    parser.add_argument('codec_folder', help='The folder in which the codec is stored')
    parser.add_argument('codec_name', help='The name of the codec to use')
    parser.add_argument('output_path', help='The path of the output file')

    args = parser.parse_args()

    codec = load_protein_codec(args.codec_name, args.codec_folder)
    encodings, context = codec[0][0], codec[1]

    compressed = []

    for file in tqdm(args.input_files, unit="file"):
        for protein in read_proteins_from_file(file):
            out = compress_sequence(protein, context, encodings)
            compressed.append(binary_string_to_utf8(out))

    # Save each compressed sequence on a new line in the output file
    with open(args.output_path, 'w', encoding='utf-8') as f:
        for seq in compressed:
            f.write(seq + '🚀🚀')

    print("Compressed all", len(compressed), "sequences")


if __name__ == "__main__":
    main()
