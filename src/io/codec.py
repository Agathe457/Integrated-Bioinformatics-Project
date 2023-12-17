import json
from typing import Dict, List

ENCODINGS_DIR = "encodings"


def store_protein_codec(encodings: List[Dict], context: int, name: str, output_folder: str = ENCODINGS_DIR):
    """
    Store the protein codec to a file.

    :param output_folder: (Optional) The folder where to store the data.
    :param encodings: The encodings to store
    :param context: The context of the encoding
    :param name: The name of the encoding
    """
    doc = ''

    # First line contains context
    doc += str(context) + "\n"

    for value in encodings:
        doc += json.dumps(value) + "\n"

    with open(output_folder + "/" + name + ".protcodec", "w") as file:
        file.write(doc)


def load_protein_codec(name: str, output_folder: str = ENCODINGS_DIR):
    """
    Load the protein codec from a file.

    :param output_folder:  The folder where the codec lies
    :param name: The name of the encoding
    :return: The encodings
    """
    with open(output_folder + "/" + name + ".protcodec", "r") as file:
        context = int(file.readline().strip())

        encodings = []

        for line in file:
            encodings.append(json.loads(line.strip()))

        return encodings, context
