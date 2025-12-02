import matplotlib.pyplot as plt
import numpy as np
import pathlib
import csv
import pandas as pd

def plot_times_changes_with_thread_increase(data, sample_size):
    data = data[data['sample_size'] == sample_size]
    plt.figure(figsize=(10, 6))
    for algorithm in data['data_name'].unique():
        subset = data[data['data_name'] == algorithm]
        plt.scatter(subset['num_of_threads'], subset['time'], s=60, alpha=0.8, label=algorithm)
    plt.title(f'Execution Time vs Number of Threads (Sample Size: {sample_size})')
    plt.xlabel('Number of Threads')
    plt.ylabel('Execution Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_times_changes_with_thread_increase_and_sequence(data, data_sequence, sample_size):
    data = data[data['sample_size'] == sample_size]
    plt.figure(figsize=(10, 6))
    for algorithm in data['data_name'].unique():
        subset = data[data['data_name'] == algorithm]
        plt.scatter(subset['num_of_threads'], subset['time'], s=60, alpha=0.8, label=algorithm)
    
    seq_subset = data_sequence[data_sequence['sample_size'] == sample_size]
    print(seq_subset)
    print(data_sequence)
    plt.scatter([0]*len(seq_subset), seq_subset['time'], s=100, alpha=0.8, label='Sequential', color='red', marker='x')

    plt.title(f'Execution Time vs Number of Threads (Sample Size: {sample_size})')
    plt.xlabel('Number of Threads')
    plt.ylabel('Execution Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.show()


def read_csv(path):
    data = pd.read_csv(path)
    return data
    

def plot_mpi_vs_no(data_mpi, data_wo, sample_size):
  
    mpi_data = data_mpi[data_mpi['sample_size'] == sample_size]
    no_mpi_data = data_wo[data_wo['sample_size'] == sample_size]

    plt.figure(figsize=(10, 6))
    plt.scatter(mpi_data['data_name'], mpi_data['time'], s=60, alpha=0.8, label='MPI', color='blue')
    plt.scatter(no_mpi_data['data_name'], no_mpi_data['time'], s=60, alpha=0.8, label='No MPI', color='orange')

    plt.title(f'MPI vs No MPI Execution Time')
    plt.xlabel('Type of Data Set')
    plt.ylabel('Execution Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":

    path_mpi = "bucket_sort/bucket_sort_mpi_wynik.csv"
    path_wo = "bucket_sort/bucket_sort_wyniki.csv"
    data_mpi = read_csv(path_mpi)
    data_wo = read_csv(path_wo)
    plot_mpi_vs_no(data_mpi, data_wo, 1000000)

    path_openMP = "merge_sort/merge_sort_open_mp_wyniki.csv"
    path_merge = "merge_sort/merge_sort_wyniki.csv"
    data_openMP = read_csv(path_openMP)
    data_merge = read_csv(path_merge)
    plot_times_changes_with_thread_increase_and_sequence(data_openMP, data_merge, 100000)

    radix = "results_radix_cuda.csv"
    radix_noo_cuda = "results_without_cuda.csv"
    data_radix = read_csv(radix)
    data_radix_no_cuda = read_csv(radix_noo_cuda)
    plot_times_changes_with_thread_increase_and_sequence(data_radix, data_radix_no_cuda, 1000000)

    find_the_bes_time(data_radix, data_openMP, data_merge, 10000)
    find_the_bes_time(data_radix, data_openMP, data_merge, 1000)
    find_the_bes_time(data_radix, data_openMP, data_merge, 1000000)
