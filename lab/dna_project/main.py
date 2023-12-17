from lib.benchmark import benchmark_compression_function
from lib.results import save_results_to_csv
from lib.samples import load_samples_generator
from methods import binary, my_new_method

METHODS = (
    # rotation_run_length_encoding,
   # binary,
    # huffman,
    # pattern,
    # group,
    my_new_method,

)

if __name__ == "__main__":
    all_results = []
    for method in METHODS:
        print(f"Launching benchmark for method : {method.__name__}...")

        results = benchmark_compression_function(
            method.compression_function,
            load_samples_generator()

        )

        all_results.append(
            (method.__name__, results)
        )

        print("== RESULTS ==")

        for key, value in results.items():
            bits_per_nucleotide = round(8 * (100-value) / 100, 2)
            print(f"  {key} : {value}% ({bits_per_nucleotide} bits per nucleotide)")

    save_results_to_csv(
        all_results,
        "out/latest.csv"
    )
