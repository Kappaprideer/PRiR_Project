from pathlib import Path
import random
    
def generate_random_data(file_path: Path, num_elements: int, value_range: int):
    with open(file_path, 'w') as file:
        for _ in range(num_elements):
            file.write(f"{random.randint(0, value_range)}\n")
    print(f"Generated {num_elements} random integers in range 0 to {value_range} at {file_path}")


def generate_almost_sorted_data(file_path: Path, num_elements: int, swaps: int):
    data = list(range(num_elements))
    for _ in range(swaps):
        i, j = random.sample(range(num_elements), 2)
        data[i], data[j] = data[j], data[i]
    file_path.write_text("\n".join(map(str, data)))
    print(f"Generated almost sorted data with {swaps} swaps at {file_path}")

def generate_data_with_duplicates(file_path: Path, num_elements: int, unique_values: int):
    data = [random.randint(0, unique_values - 1) for _ in range(num_elements)]
    file_path.write_text("\n".join(map(str, data)))
    print(f"Generated {num_elements} integers with {unique_values} unique values at {file_path}")

if __name__ == "__main__":

    for numbers_count in [1000, 100000, 1000000]:
        generate_random_data(Path(f"data/random_data_{numbers_count}.txt"), numbers_count, numbers_count)
        generate_almost_sorted_data(Path(f"data/almost_sorted_data_{numbers_count}.txt"), numbers_count, 100)
        generate_data_with_duplicates(Path(f"data/data_with_duplicates_{numbers_count}.txt"), numbers_count, 20)
    