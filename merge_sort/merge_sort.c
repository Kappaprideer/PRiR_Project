#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define NUM_FILES 9

// Scalanie dwóch posortowanych fragmentów
void merge(int *arr, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;

    int *L = malloc(n1 * sizeof(int));
    int *R = malloc(n2 * sizeof(int));

    for (int i = 0; i < n1; i++) L[i] = arr[left + i];
    for (int j = 0; j < n2; j++) R[j] = arr[mid + 1 + j];

    int i = 0, j = 0, k = left;

    while (i < n1 && j < n2) {
        if (L[i] <= R[j])
            arr[k++] = L[i++];
        else
            arr[k++] = R[j++];
    }

    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];

    free(L);
    free(R);
}

// Rekurencyjny merge sort z ograniczeniem głębokości równoległości
void merge_sort_limited(int *arr, int left, int right, int depth, int max_depth) {
    if (left >= right) return;

    int mid = (left + right) / 2;

    if (depth < max_depth) {
        merge_sort_limited(arr, left, mid, depth + 1, max_depth);

        merge_sort_limited(arr, mid + 1, right, depth + 1, max_depth);

    } else {
        merge_sort_limited(arr, left, mid, depth + 1, max_depth);
        merge_sort_limited(arr, mid + 1, right, depth + 1, max_depth);
    }

    merge(arr, left, mid, right);
}


// --- WCZYTYWANIE LICZB Z PLIKU ---
int* load_numbers(const char *filename, int *count) {
    FILE *f = fopen(filename, "r");
    if (!f) {
        perror("Nie można otworzyć pliku");
        exit(1);
    }

    int capacity = 1024;
    int *arr = malloc(capacity * sizeof(int));
    *count = 0;

    while (fscanf(f, "%d", &arr[*count]) == 1) {
        (*count)++;
        if (*count >= capacity) {
            capacity *= 2;
            arr = realloc(arr, capacity * sizeof(int));
        }
    }

    fclose(f);
    return arr;
}


int extract_number_from_filename(const char *filename) {
    // Szukamy pierwszej liczby w nazwie pliku
    int number = 0;
    while (*filename) {
        if (isdigit(*filename)) {
            number = atoi(filename);
            break;
        }
        filename++;
    }
    return number;
}

int main() {

    printf("data_name,sample_size,time,num_of_threads\n");
    const char *files[NUM_FILES] = {
        "../data/almost_sorted_data_1000.txt",
        "../data/almost_sorted_data_100000.txt",
        "../data/almost_sorted_data_1000000.txt",
        "../data/data_with_duplicates_1000.txt",
        "../data/data_with_duplicates_100000.txt",
        "../data/data_with_duplicates_1000000.txt",
        "../data/random_data_1000.txt",
        "../data/random_data_100000.txt",
        "../data/random_data_1000000.txt"
    };
    
    for (int idx = 0; idx < NUM_FILES; idx++)
    {
        int n;
        int *arr = load_numbers(files[idx], &n);

        int max_depth = 20;

        double start = omp_get_wtime();
        merge_sort_limited(arr, 0, n - 1, 0, max_depth);
        double end = omp_get_wtime();

        int number_from_filename = extract_number_from_filename(files[idx]);
        char* data_name = idx > 2 ? (idx > 5 ? "duplicated" : "random") : "almost_sorted";

        printf("%s,%d,%.6f,1\n", data_name, number_from_filename, (end-start));

        free(arr);
    }

    return 0;
}
