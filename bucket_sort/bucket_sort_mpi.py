import mpi4py.MPI as MPI
import time
import pathlib

def get_data(file_path):
    with open(file_path, 'r') as f:
        lst = [int(line.strip()) for line in f]
    return lst

def bucket_sort(list, num_buckets):
    if len(list) == 0:
        return list

    min_value = min(list)
    max_value = max(list)

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


if __name__ == "__main__":

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    workdir = pathlib.Path(__file__).parent.parent
    data_path = workdir / "data/data_with_duplicates.txt"
    

    if rank == 0:
        data = get_data(data_path)
        start_time = time.time()

        min_value = min(data)
        max_value = max(data)
    else:
        data = None
        min_value = None
        max_value = None
        start_time = None

    min_value = comm.bcast(min_value, root=0)
    max_value = comm.bcast(max_value, root=0)

    if rank == 0:
        bucket_range = (max_value - min_value + 1) / size
        buckets = [[] for _ in range(size)]

        for value in data:
            index = int((value - min_value) / bucket_range)
            if index == size:
                index -= 1
            buckets[index].append(value)
    else:
        buckets = None

    local_data = comm.scatter(buckets, root=0)
    k = 4

    local_sorted = bucket_sort(local_data, k)

    gathered = comm.gather(local_sorted, root=0)

    if rank == 0:
        final_sorted = [x for sublist in gathered for x in sublist]
        print("Execution time:", time.time() - start_time)