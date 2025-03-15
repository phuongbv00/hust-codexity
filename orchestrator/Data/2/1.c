In C++, the `new` and `delete` operators are used for dynamic memory allocation and deallocation, respectively. 

- **`new` Operator**: This operator allocates memory on the heap for a variable or an array of variables. It returns a pointer to the beginning of the allocated memory block. The memory allocated using `new` persists until it is explicitly deallocated using `delete`. The syntax for using `new` is as follows:

  ```cpp
  int* ptr = new int; // Allocates memory for a single integer
  int* arr = new int[10]; // Allocates memory for an array of 10 integers
  ```

- **`delete` Operator**: This operator is used to deallocate memory that was previously allocated with `new`. It frees up the memory, making it available for future allocations. The syntax for using `delete` is as follows:

  ```cpp
  delete ptr; // Deallocates memory for a single integer
  delete[] arr; // Deallocates memory for an array of integers
  ```

Using `new` and `delete` helps manage memory manually, allowing for more control over resource allocation. However, it also requires careful management to avoid memory leaks (forgetting to deallocate memory) and dangling pointers (deallocating memory that is still in use).