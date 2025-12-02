from pathlib import Path
import pathlib
import time

def bucket_sort(list: list[int], num_buckets: int) -> list[int]:
    if len(list) == 0:
        return list

    min_value = min(list)
    max_value = max(list)

    if min_value == max_value:
        return list

    bucket_range = (max_value - min_value) / num_buckets
    buckets = [[] for _ in range(num_buckets)]

    for value in list:
        index = int((value - min_value) / bucket_range)
        if index == num_buckets:
            index -= 1
        buckets[index].append(value)

    sorted_list = []
    for bucket in buckets:
        sorted_list.extend(sorted(bucket))

    return sorted_list

def get_data(path:Path) -> list[int]:
    text = path.read_text()
    lst = [int(line) for line in text.splitlines()]
    return lst

if __name__ == "__main__":
    start_time = time.time()
    workdir = pathlib.Path(__file__).parent.parent
    data_path = workdir / "data/random_data.txt"
    data = get_data(data_path)
    num_buckets = 4
    sorted_data = bucket_sort(data, num_buckets)
    print("Execution time:", time.time() - start_time)