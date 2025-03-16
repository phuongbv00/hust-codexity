#include <stdio.h>
#include <stdlib.h>

void createSieve(int length, int width) {
    int **sieve = malloc(length * sizeof(int *));
    for (int i = 0; i < length; i++) {
        sieve[i] = malloc(width * sizeof(int));
    }

    // Initialize the sieve with some values (for demonstration)
    for (int i = 0; i < length; i++) {
        for (int j = 0; j < width; j++) {
            sieve[i][j] = 0; // You can set this to any value you need
        }
    }

    // Example operation: Fill the sieve with values
    for (int i = 0; i < length; i++) {
        for (int j = 0; j < width; j++) {
            sieve[i][j] = i * width + j; // Just a simple formula for demonstration
        }
    }

    // Print the sieve
    for (int i = 0; i < length; i++) {
        for (int j = 0; j < width; j++) {
            printf("%d ", sieve[i][j]);
        }
        printf("\n");
    }

    // Free the allocated memory
    for (int i = 0; i < length; i++) {
        free(sieve[i]);
    }
    free(sieve);
}

int main() {
    int length = 5;
    int width = 5;
    createSieve(length, width);
    return 0;
}