import json
from typing import Dict, List

ENCODINGS_DIR = "encodings"


def store_protein_codec(encodings: List[Dict], context: int, name: str):
    """
    Store the protein codec to a file.

    :param encodings: The encodings to store
    :param context: The context of the encoding
    :param name: The name of the encoding
    """
    doc = ''

    # First line contains context
    doc += str(context) + "\n"

    for value in encodings:
        doc += json.dumps(value) + "\n"

    with open(ENCODINGS_DIR + "/" + name + ".protcodec", "w") as file:
        file.write(doc)


def load_protein_codec(name: str) -> (List[Dict], int):
    """
    Load the protein codec from a file.

    :param name: The name of the encoding
    :return: The encodings
    """
    with open(ENCODINGS_DIR + "/" + name + ".protcodec", "r") as file:
        context = int(file.readline().strip())

        encodings = []

        for line in file:
            encodings.append(json.loads(line.strip()))

        return encodings, context
