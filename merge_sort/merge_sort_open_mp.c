#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

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
        #pragma omp task shared(arr)
        merge_sort_limited(arr, left, mid, depth + 1, max_depth);

        #pragma omp task shared(arr)
        merge_sort_limited(arr, mid + 1, right, depth + 1, max_depth);

        #pragma omp taskwait
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

int main() {

    char filename[] = "../data/data_with_duplicates.txt";
    int n;
    // int *arr = malloc(n * sizeof(int));

    int *arr = load_numbers(filename, &n);
    // Losowe wartości
    // for (int i = 0; i < n; i++) {
    //     arr[i] = rand() % 1000000;
    // }

    printf("Przed sortowaniem:\n");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");

    int max_depth = 10;

    double start = omp_get_wtime();

    // Uruchom sortowanie w kontekście równoległym
    #pragma omp parallel
    {
        #pragma omp single
        merge_sort_limited(arr, 0, n - 1, 0, max_depth);
    }

    double end = omp_get_wtime();

    printf("Po sortowaniu:\n");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");

    printf("Czas sortowania: %.6f sekund\n", end - start);

    free(arr);
    return 0;
}
