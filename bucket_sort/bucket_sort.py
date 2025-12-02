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
    print("data_name,sample_size,time")

    for number in [1000, 100000, 1000000]:
        for name in ["almost_sorted_data", "data_with_duplicates", "random_data"]:
            sum = 0
            for _ in range(10):

                workdir = pathlib.Path(__file__).parent.parent
                data_path =  f"../data/{name}_{number}.txt"
                with open(data_path, 'r') as f:
                    data = [int(line.strip()) for line in f]
                        
                num_buckets = 4

                start_time = time.time()

                sorted_data = bucket_sort(data, num_buckets)
                
                end_time = time.time()

                execution_time = end_time - start_time
                sum += execution_time
    
            print(f"{name},{number},{sum/10:.6f}")