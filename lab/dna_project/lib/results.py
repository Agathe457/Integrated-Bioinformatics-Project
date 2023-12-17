from typing import List, Tuple

from lib.typedefs import Result


def save_results_to_csv(results: List[Tuple[str, Result]], output_path: str) -> str:
    lines = []

    for method, result in results:
        lines.append(method)
        for test_name, percentage in result.items():
            lines.append(f"{test_name},{percentage}")
        lines.append("\n")

    with open(output_path, 'w') as output_file:
        output_file.write("\n".join(lines))

    return output_path
