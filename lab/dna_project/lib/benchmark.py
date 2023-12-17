from typing import Callable, Generator

from lib.measure import measure_on_disk_size
from lib.typedefs import DNA, BytesOrString, Result


def benchmark_compression_function(compression_function: Callable[[DNA], BytesOrString],
                                   samples: Generator[str, None, None]) -> Result:
    results = {}

    for sample, sample_data in samples:
        compressed_sample = compression_function(sample_data)

        if isinstance(compressed_sample, BytesOrString):
            size = measure_on_disk_size(compressed_sample)
        else:
            raise NotImplementedError(f"The compress function {compression_function} should not"
                                      f"return a value of type {type(compressed_sample)}")

        original_size = measure_on_disk_size(sample_data)
        compression_ratio = round(size / original_size * 100, 2)

        results[sample] = round(100 - compression_ratio, 2)

    return results
