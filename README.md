# Integrated-Bioinformatics-Project

Group 9: Gaspard Merten, Ebru Ataman, Camillo Colleluori, Agathe Pourprix

Transforming Proteomic Data Compression.
Overcoming Compression Challenges and Innovat-ing New Combinatorial Techniques: Accessible Analysis and Computational
Efficiency.

Link to report: https://1drv.ms/w/s!AkttQi26dAy4glH1RECYG2jUP1U0

## Structure of the project

## The _src_ folder

The src folder is where the core logic of the last iteration of the
compression algorithm lies. It is composed of well-thought and documented
code.

## The _scripts_ folder

The scripts folder contains various scripts used in the project.

### Build generic encoding

This script generates a huffman encoding based on the compressed
result of the multi-level encodings. It uses proteins from all
proteomes, compresses them, and then use the compressed result
to generate a new encoding table. This table will then be used
by the compressor to further increase the compression rate.

### Build global AA encoding

Sometimes, an amino acid can be missing from a multi-level table, especially
when the context is high. In such cases, this global AA encoding, which is built
using proteins from 100 proteomes, can offer better compression than the 5 bits / AA
standard encoding.

### Download all proteomes (bash)

This bash script can download 100 proteomes from UniProt automatically.
This allows not to push the proteomes to the git, but instead to download them
locally once needed.

### Benchmark folder

The benchmark folder contains various scripts that are used to
benchmark the performance of the compression algorithm in different settings.

## The _bin_ folder

The bin folder contains python scripts meant for usage in external
environment. They allow to generate a codec, to compress proteins with it,
and to decompress them afterwards.

## The _source_ folder

This folder contains generic.encoding and global_huffman.encoding, generated
using the scripts mentioned previously.