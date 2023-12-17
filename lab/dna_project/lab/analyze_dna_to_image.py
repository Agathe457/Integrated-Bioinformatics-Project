import io

import numpy as np
from PIL import Image

# grayscale images are 256 values per pixel
# 256 is 2^8 so we can represent 4 nucleotides with 1 pixel
CONV = {
    "A": "00",
    "C": "01",
    "G": "10",
    "T": "11"
}


def dna_to_binary(dna_sequence: str) -> str:
    binary_sequence = ""
    for nucleotide in dna_sequence:
        binary_sequence += CONV[nucleotide]
    return binary_sequence


def binary_to_pixel(binary_sequence: str) -> int:
    data = []

    for i in range(0, len(binary_sequence), 8):
        # Convert the binary sequence to an actual number
        data.append(int(binary_sequence[i:i + 8], 2))

    # Round up to the nearest multiple of 256
    data = data + [0] * (256 - len(data) % 256)

    # Split into windows of 256*256
    data = [
        data[i:i + 256]
        for i in range(0, len(data), 256)
    ]

    # Convert data to an image
    image = Image.fromarray(np.array(data, dtype=np.uint8), 'L')
    # plot image
    image.show()
    # Save image to a buffer
    buffer = io.BytesIO()

    image.save(buffer, format="PNG")

    # Get the binary data from the buffer
    return buffer.getvalue()
