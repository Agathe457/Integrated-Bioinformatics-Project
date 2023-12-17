import argparse

from tqdm import tqdm

from src.generation.build_encodings import build_codec
from src.io.codec import store_protein_codec
from src.io.read_proteins import read_proteins_from_file


def main():
    parser = argparse.ArgumentParser(description='Generate a compression codec from source proteins')
    parser.add_argument('input_files', nargs='+', help='Input file paths')
    parser.add_argument('output_folder', help='Output file folder')
    parser.add_argument('context', help='The size of the context')
    parser.add_argument('name', help='The name of the codec (used as file name)')
    parser.add_argument('format', help='The source files format', default="fasta")

    args = parser.parse_args()

    proteins = []

    for file in tqdm(args.input_files, unit="file"):
        proteins += read_proteins_from_file(file, args.format)

    codec = build_codec([proteins], int(args.context))
    store_protein_codec(codec, args.context, args.name, output_folder=args.output_folder)

    print(f"Codec {args.name} has been generated")


if __name__ == "__main__":
    main()
