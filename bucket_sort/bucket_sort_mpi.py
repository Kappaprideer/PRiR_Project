import mpi4py.MPI as MPI
import time
import pathlib
import sys

def bucket_sort(input_list, num_buckets):
    if not input_list:
        return []

    min_value = min(input_list)
    max_value = max(input_list)

    if min_value == max_value:
        return input_list

    bucket_range = (max_value - min_value) / num_buckets
    buckets = [[] for _ in range(num_buckets)]

    for value in input_list:
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

    buckets = None
    data = None
    print("data_name,sample_size,time,num_of_processes")
    comm = MPI.COMM_WORLD
    process_size = comm.Get_size()

    for number in [1000, 100000, 1000000]:
        for name in ["almost_sorted_data", "data_with_duplicates", "random_data"]:
            sum = 0
            for _ in range(10):
                if rank == 0:
                    try:
                        workdir = pathlib.Path(__file__).parent.parent
                        data_path =  f"../data/{name}_{number}.txt"
                            
                        with open(data_path, 'r') as f:
                            data = [int(line.strip()) for line in f]
                            
                    except Exception as e:
                        print(f"Error reading file: {e}")
                        sys.exit(1)

                    start_time = time.time()
                    
                    min_value = min(data)
                    max_value = max(data)

                    bucket_range = (max_value - min_value + 1) / size
                    buckets = [[] for _ in range(size)]

                    for value in data:
                        index = int((value - min_value) / bucket_range)
                        if index == size:
                            index -= 1
                        buckets[index].append(value)
                        

                local_data = comm.scatter(buckets, root=0)
                local_sorted = bucket_sort(local_data, num_buckets=4) 
                gathered = comm.gather(local_sorted, root=0)

                if rank == 0:
                    final_sorted = [x for sublist in gathered for x in sublist]
                    end_time = time.time()

                    sum += end_time - start_time

            print(f"{name},{number},{sum/10:.6f},{process_size}")