import argparse
import logging

from tqdm import tqdm

from src.compress.binary_utf8 import utf8_to_binary_string
from src.compress.compress_sequence import decompress_sequence
from src.io.codec import load_protein_codec
from src.utils.huffman import encoding_to_decoding_codes


def _read_compressed_sequences_from_file(file: str):
    with open(file, "r", encoding='utf-8') as f:
        return f.read().split('🚀🚀')


def main(limit=None):
    parser = argparse.ArgumentParser(description='Compress AA sequences from input files')
    parser.add_argument('input_files', nargs='+', help='Input file paths')
    parser.add_argument('codec_folder', help='The folder in which the codec is stored')
    parser.add_argument('codec_name', help='The name of the codec to use')
    parser.add_argument('output_path', help='The path of the output file')
    args = parser.parse_args()

    codec = load_protein_codec(args.codec_name, args.codec_folder)
    encodings, context = codec[0][0], codec[1]
    decodings = encoding_to_decoding_codes(encodings)

    decompressed = []

    for file in tqdm(args.input_files, unit="file"):
        compressed_sequences = _read_compressed_sequences_from_file(file)
        for i, compressed_seq in enumerate(compressed_sequences):
            binary_seq = utf8_to_binary_string(compressed_seq)
            decompressed_seq = decompress_sequence(binary_seq, context, decodings)
            decompressed.append(decompressed_seq)

            if i == limit:
                break
    # Save each decompressed sequence on a new line in the output file
    with open(args.output_path, 'w') as f:
        for seq in decompressed:
            f.write(seq + '\n')

    print("Decompressed", len(decompressed), 'proteins')


if __name__ == '__main__':
    main()
