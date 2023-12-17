from typing import Generator


def read_proteins_from_file(path: str, extension=None) -> Generator[str, None, None]:
    """
    Read proteins from a file.

    :param path: The path to the file
    :param extension: The extension of the file (optional, will be inferred if not provided)
    :return: A generator of proteins
    """

    if extension is None:
        extension = path.split(".")[-1]

    if extension == "fasta":
        with open(path, "r") as fasta_file:
            buffer = ""
            for line in fasta_file:
                if line[0] == ">":
                    if buffer:
                        yield buffer
                        buffer = ""
                    continue
                else:
                    buffer += line.strip()

            if buffer:
                yield buffer

    elif extension == "tsv":
        with open(path, "r") as tsv_file:
            for c, line in enumerate(tsv_file):
                if c == 0:
                    continue
                yield line.split("\t")[-1].strip()
    else:
        raise ValueError("Invalid file extension: " + str(extension))
