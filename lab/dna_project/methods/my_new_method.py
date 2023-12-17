import io

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

# grayscale images are 256 values per pixel
# 256 is 2^8 so we can represent 4 nucleotides with 1 pixel
CONV = {
    "A": "00",
    "C": "10",
    "G": "01",
    "T": "11"
}
INVERSE_CONV = {
    "00": "A",
    "01": "C",
    "10": "G",
    "11": "T"
}


def dna_to_binary(dna_sequence: str) -> str:
    binary_sequence = ""
    for nucleotide in dna_sequence:
        binary_sequence += CONV[nucleotide]
    return binary_sequence


def compression_function(dna_sequence: str) -> int:
    binary_sequence = dna_to_binary(dna_sequence)

    width = 148

    data = []

    for i in range(0, len(binary_sequence), 8):
        # Convert the binary sequence to an actual number
        data.append(int(binary_sequence[i:i + 8], 2))

    # Round up to the nearest multiple of 256
    data = data + [0] * (width - len(data) % width)

    # Replace the 10 least common elements with the most common one

    # Split into windows of width*width
    data = [
        data[i:i + width]
        for i in range(0, len(data), width)
    ]

    # 

    def flatten(l):
        for el in l:
            if isinstance(el, list):
                yield from flatten(el)
            else:
                yield el

    # Compute histogram from data
    plt.hist(list(flatten(data)), bins=256)
    plt.show()

    # Convert data to an image
    image = Image.fromarray(np.array(data, dtype=np.uint8), 'L')
    # Save image to a buffer
    buffer = io.BytesIO()

    image.save(buffer, format="WEBP", lossless=True)

    # Plot correlation matrix of the image
    plt.imshow(np.array(data, dtype=np.uint8), cmap='gray', vmin=0, vmax=255)
    plt.show()

    # save image to out/x.webp
    image.save(f"out/{dna_sequence[:10]}.webp", format="WEBP", lossless=True)

    return buffer.getvalue()
